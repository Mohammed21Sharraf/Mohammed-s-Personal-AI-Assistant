from fastapi import APIRouter, HTTPException
from .services import generate_response
from .models import QueryRequest

router = APIRouter()

@router.post("/query")
async def query_model(request: QueryRequest):
    """API endpoint to answer questions based on CV, research papers, and GitHub repos."""
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    response = generate_response(request.question)
    return {"answer": response["answer"], "context": response["context"]}
