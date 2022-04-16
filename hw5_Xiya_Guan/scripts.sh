# load fasttext embeddings that are trained on wiki news. Each embedding has 300 dimensions
python -m embedding_service.server --embedding fasttext  --model pa5_data/wiki-news-300d-1M-subword.vec

# load sentence BERT embeddings that are trained on msmarco. Each embedding has 768 dimensions
python -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3

# load wapo docs into the index called "wapo_docs_50k"
python load_es_index.py --index_name wapo_docs_50k --wapo_path pa5_data/subset_wapo_50k_sbert_ft_filtered.jl


python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 397 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 433 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 816 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 442 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 822 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 806 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 805 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 690 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --use_english_analyzer True --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --use_english_analyzer True --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --use_english_analyzer True --vector_name ft_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --top_k 20
python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --vector_name sbert_vector --top_k 20  --search_type rerank
python evaluate.py --index_name wapo_docs_50k --topic_id 336 --query_type kw --vector_name ft_vector --top_k 20  --search_type rerank

