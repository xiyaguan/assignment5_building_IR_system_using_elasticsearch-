# assignment5_building_IR_system_using_elasticsearch

Research on alternative approaches to document indexing and querying. with the help of Elasticsearch.


## Basic Information
- Title: Building a retrieval system using elasticsearch
- Author: Xiya Guan
- Date: April 15th, 2022
- Description: implement a vector space information retrieval system using elasticsearch.


## Input
Our BM25 retrieval system defaults to use keyword text and falls back to query text if no keyword text is provided. If neither keyword nor query text is provided, the program will jump back to home page.

## Reranking architecture
The elastic search system defaults to retrieve relevant documents using bm25. After retrieving top k relevant documents, users can utilize query representative and doc representative using pretrained word embeddings (either sentence bert embeddings or fastText embeddings) to rerank the retrieved top k docs.

## Analyzer
User can choose different analyzers to anlalyze input text. Here we provide two analyzers -- Standard analyzer and English analyzer.

## Output

For each query in the provided 12 queries, here is the result table with 1 row per search type and 1 column per query type. The value of each cell is the NDCG@20 value.  \
![Screen Shot 2022-04-15 at 10 37 42 PM](https://user-images.githubusercontent.com/79282489/163658333-19858413-ed87-49e2-a39e-f0cdab1622f1.png) \
\
![Screen Shot 2022-04-15 at 10 38 09 PM](https://user-images.githubusercontent.com/79282489/163658334-62153b24-d3ac-407e-b5a9-8361045473a8.png) \
\
![Screen Shot 2022-04-15 at 10 38 21 PM](https://user-images.githubusercontent.com/79282489/163658335-3c18c080-55c4-44a4-9544-cf2c540a4035.png)

### Observations
1. Using pretrained vector does not necessarily gaurantee a good performance.
2. Different topics have different difficulty level.

## Web UI Home Page

Below is the screenshot for our Web UI Home Page.
![Screen Shot 2022-04-15 at 9 19 17 PM](https://user-images.githubusercontent.com/79282489/163656287-68b065b3-c963-4f6f-ab44-902f8ae698b8.png)


## Web UI Result Page

Below is the screenshot for our Web UI Result Page, note that 

1. the title link shows underline when cursor hovers over.
2. the snippets highlights the keywords in the reranking query.

![Screen Shot 2022-04-15 at 9 20 05 PM](https://user-images.githubusercontent.com/79282489/163656310-a2e7fb42-7e1c-49d3-8fd7-2c629ba957b3.png)




## Dependencies and Build Instructions
### 1 Install Dependencies
The required packages are listed in [requirements.txt](requirements.txt).
```shell script
pip install -r requirements.txt
```
### 2 Set up ElasticSearch Server
Download ES from https://www.elastic.co/downloads/past-releases#elasticsearch. Make sure you are choosing Elasticsearch 7.10.2 (used for scoring the assignment). To start the ES engine:

```shell script
cd elasticsearch-7.10.2/
./bin/elasticsearch
```

### 3 Download all Data

Your [data/](data/) directory should contain the following files, so that you can run the system properly:

```
data
├── pa5_queries.json
├── subset_wapo_50k_sbert_ft_lf_filtered.jl
├── topics2018.xml
└── wiki-news-300d-1M-subword.vec
```

You can download ```wiki-news-300d-1M-subword.vec``` at [here](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip).

[subset_wapo_50k_sbert_ft_filtered.jl](https://drive.google.com/file/d/1h1LDoLRBgQgUJH5tbWuBlG-dparXy6f-/view?usp=sharing): JSON line file containing a subset of documents in TREC, including their sBERT, fastText, and Longformer vectors

### 4 Build Index

To load wapo docs into the index called "wapo_docs_50k_lf", run:
```shell script
python load_es_index.py --index_name wapo_docs_50k_lf --wapo_path data/subset_wapo_50k_sbert_ft_lf_filtered.jl
```


### 5 Setting up Embedding Servers

You don’t need to download any pretrained model for sentence transformers, it will be loaded the first time it's called.

- Load fasttext model (click [this](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip) link to download `.vec` file first,  then put it into `data/` folder):

```shell script
python -m embedding_service.server --embedding fasttext  --model data/wiki-news-300d-1M-subword.vec
```

- Load sbert model:

```shell script
python -m embedding_service.server --embedding sbert --model msmarco-distilbert-base-v3
```


### 6 Running the Programs

- For Evaluation: 
    ```shell script
    python evaluate.py 
    ```
    Experiment on different argments please check out ```scripts.sh```

- For the web app:

    Run the hw5.py, then type http://127.0.0.1:5000/ in the browser to view the web application.
    
    ```shell script
    python hw5.py 
    ```

