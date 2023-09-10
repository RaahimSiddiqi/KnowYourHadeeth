# Use this file for actually making the queries 
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from pprint import pprint

sbert = HuggingFaceEmbeddings(model_name="sentence-transformers/msmarco-bert-base-dot-v5")
vectordb = Chroma(
  embedding_function = sbert,
  persist_directory = 'chroma_store_scraper_msmarco_bert_base_dot_v5'
)

print("searching...")
results = vectordb.similarity_search_with_score("What is Qasr Prayer during travel?", k=10, search_type="hybrid")
pprint(results)