from .vectorstore import load_vector_store
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from .config import GROQ_API_KEY

vector_db = load_vector_store()
retriever = vector_db.as_retriever(
)

llm = ChatGroq(api_key=GROQ_API_KEY, model_name="deepseek-r1-distill-llama-70b")

prompt = ChatPromptTemplate.from_template("""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.


<context>
{context}
</context>

Question: {input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

def generate_response(question: str):
    """Retrieves relevant context & queries Groq LLM."""
    response = retrieval_chain.invoke({"input": question})
    return response
