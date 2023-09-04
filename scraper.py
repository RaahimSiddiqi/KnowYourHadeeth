# This file is used to read the output.json from the hadithscraper, make them into documents
# and add them to a persisted vector db

import json
from tqdm import tqdm
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

documents = []
file = open("hadithscraper\hadithscraper\spiders\output.json", encoding="utf8")
data = json.load(file)[:10]

for hadith in data:
    metadata = dict(narrator=hadith["narrator"], author=hadith["author"], reference=hadith["reference"])
    documents.append(Document(page_content=hadith["text"], metadata=metadata))

sbert = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectordb = Chroma(
  embedding_function = sbert,
  persist_directory = 'chroma_store_scraper'
)
vectordb.persist()

for doc in tqdm(documents):
  vectordb.add_documents([doc])