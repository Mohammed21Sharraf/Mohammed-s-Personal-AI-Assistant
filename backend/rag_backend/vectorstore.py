import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from .config import VECTOR_DB_PATH

def load_pdfs(folder_path):
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            doc_texts = loader.load()
            doc_type = "Mohammed_Sharraf_CV_2025" if "Mohammed_Sharraf_CV_2025" in file.lower() else "research" if "research" in file.lower() else "general"
            
            # Attach metadata
            for doc in doc_texts:
                doc.metadata = {"source": doc_type}  
            
            documents.extend(doc_texts)
    print(documents)
    return documents


def initialize_vector_store():
    embeddings = OllamaEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    
    docs = load_pdfs("data/")
    chunked_docs = text_splitter.split_documents(docs)
    
    vector_db = FAISS.from_documents(chunked_docs, embeddings)
    vector_db.save_local(VECTOR_DB_PATH)
    return vector_db

def load_vector_store():
    if os.path.exists(VECTOR_DB_PATH):
        return FAISS.load_local(
            VECTOR_DB_PATH,
            OllamaEmbeddings(model="llama2"),
            allow_dangerous_deserialization=True
        )
    else:
        return initialize_vector_store()
            