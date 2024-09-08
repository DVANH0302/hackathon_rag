from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from llama_index.core import VectorStoreIndex
from pydantic import BaseModel
import openai
from ..config import OPENAI_API_KEY
from app.rag.llama_index_setup import get_vector_store, initialize_llamaindex
import openai


openai.api_key = OPENAI_API_KEY

router = APIRouter()

class Query(BaseModel):
    text: str

@router.post("/query/")
async def query_documents(query: Query, db: Session = Depends(get_db)):
    try:
        query_engine = initialize_llamaindex()
        response = query_engine.query(query.text)
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")