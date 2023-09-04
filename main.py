import os
from tqdm import tqdm
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

folder_contents = os.listdir("files")
file_paths = [os.path.join("files", item) for item in folder_contents if os.path.isfile(os.path.join("files", item))]

documents = []

for file in tqdm(file_paths):
    pdf_loader = PyPDFLoader(file)
    documents.extend(pdf_loader.load())


text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(documents)

sbert = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectordb = Chroma(
  embedding_function = sbert,
  persist_directory = 'chroma_store'
)
vectordb.persist()

for doc in tqdm(documents):
  vectordb.add_documents([doc])