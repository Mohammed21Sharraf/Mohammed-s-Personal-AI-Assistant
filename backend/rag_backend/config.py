import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VECTOR_DB_PATH = "vectorstore/faiss_index"