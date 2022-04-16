import argparse
from typing import List, Any
from elasticsearch_dsl import Search
from metrics import Score
from utils import load_12_queries
from elasticsearch_dsl.query import Match, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections
from embedding_service.client import EmbeddingClient
# import csv


def generate_script_score_query(query_vector: List[float], vector_name: str) -> Query:
    """
    generate an ES query that match all documents based on the cosine similarity
    :param query_vector: query embedding from the encoder
    :param vector_name: embedding type, should match the field name defined in BaseDoc ("ft_vector" or "sbert_vector")
    :return: an query object
    """
    q_script = ScriptScore(
        query={"match_all": {}},  # use a match-all query
        script={  # script your scoring function
            "source": f"cosineSimilarity(params.query_vector, '{vector_name}') + 1.0",
            # add 1.0 to avoid negative score
            "params": {"query_vector": query_vector},
        },
    )
    return q_script


def search(index: str, query: Query, k: int) -> List[Any]:
    s = Search(using="default", index=index).query(query)[
        :k
        ]  # initialize a query and return top five results
    response = s.execute()
    return response


def _rerank_query(query_text: str, embed_methods: str, response: List[Any]) -> Query:

    if embed_methods == "ft_vector":
        encoder = EmbeddingClient(host="localhost", embedding_type="fasttext")
    elif embed_methods == "sbert_vector":
        encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
    else:
        raise NotImplementedError(embed_methods)

    query_vector = encoder.encode([query_text], pooling="mean").tolist()[
        0
    ]  # get the query embedding and convert it to a list

    # q_vector: cosine similarity between the embeddings of query text and content text.
    q_vector = generate_script_score_query(
        query_vector, embed_methods
    )  # custom query that scores documents based on cosine similarity

    # get doc ids from response
    q_match_ids = Ids(values=[hit.meta.id for hit in response])
    # print(q_match_ids)
    q_c = (
            q_match_ids & q_vector
    )  # compound query by using logic operators on retrieved ids and query vector

    return q_c


def get_score(response: List[Any], topic_id: str, k: int) -> Score:
    relevance = []
    for hit in response:
        if hit.annotation == f"{topic_id}-1":
            relevance.append(1)
        elif hit.annotation == f"{topic_id}-2":
            relevance.append(2)
        else:
            relevance.append(0)
    S = Score.eval(relevance, k)
    return S

def get_response(index_name: str,
                 query_text: str,
                 keyword_text: str,
                 use_standard_analyzer: bool,
                 embed_methods: str = "bm25",
                 k: int = 20) -> List[Any]:

    reranking = (embed_methods != "bm25")

    top_k_query = keyword_text if keyword_text else query_text
    assert top_k_query
    if use_standard_analyzer:
        q_basic = Match(
            content={"query": top_k_query}
        )  # a query that matches text in the content field of the index, using BM25 as default
    else:
        q_basic = Match(
            stemmed_content={"query": top_k_query}
        )

    response = search(
        index_name, q_basic, k
    )  # search, change the query object to see different results

    # rerank top k response
    if reranking:
        # rerank ONLY if query text is not empty prevent fasttext NaN score problem
        assert top_k_query, f"Reranking with {embed_methods} can only happen if query text is not empty!"
        # embedding: fasttext or sentence bert
        q_c = _rerank_query(top_k_query, embed_methods, response)
        response = search(
            index_name, q_c, k,
        )  # re-ranking

    return response


def main():
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index_name", required=True, type=str, help="name of the ES index"
    )
    parser.add_argument(
        "--topic_id", required=True, type=str, help="topic id number"
    )
    parser.add_argument(
        "--query_type", required=True, type=str, help="use 'kw' for keyword or 'nl' for natural language query"
    )
    parser.add_argument(
        "--search_type", type=str,
        help=" 'rerank' or 'rank' with vector only"
    )

    parser.add_argument(
        "--use_english_analyzer", help="use english analyzer for search"
    )

    parser.add_argument(
        "--vector_name", type=str,
        help="use fasttext or sbert embedding"
    )
    parser.add_argument(
        "--top_k", required=True, type=int, default=20, help="evaluate on top K ranked documents"
    )

    args = parser.parse_args()

    # load pa5_queries
    query_json_file = "pa5_data/pa5_queries.json"
    data = load_12_queries(query_json_file)

    # keywords and query text
    keywords_text = ""
    if args.query_type == "kw":
        keywords_text = data[args.topic_id]['kw']
    query_text = data[args.topic_id]['nl']

    # use english analyzer or not
    use_standard_analyzer = True
    if args.use_english_analyzer:
        use_standard_analyzer = False

    print(f"english: {args.use_english_analyzer}")
    print(f" use_standard_analyzer:{use_standard_analyzer}")

    # use reranking or not
    if args.search_type == "rerank":
        vector_name = args.vector_name
    else:
        vector_name = "bm25"

    print(args.index_name)
    print(query_text)
    print(keywords_text)
    print(f"use_standard_analyzer:{use_standard_analyzer}")
    print(vector_name)
    print(args.top_k)
    response = get_response(args.index_name, query_text, keywords_text, use_standard_analyzer, vector_name, args.top_k)
    ndcg_score = get_score(response, args.topic_id, args.top_k).ndcg
    # for hit in response:
    #     print(
    #         hit.meta.id, hit.meta.score, hit.annotation, hit.title, sep="\t"
    #     )
    print(f"topic: {args.topic_id}, score: {ndcg_score:.5f}")

if __name__ == "__main__":
    main()