# app/apis/generate_embedding.py
from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI API configuration
embedding_endpoint = "/embeddings"  # Update endpoint if necessary
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

router = APIRouter()

@router.post("/generate-embedding/")
async def generate_embedding(chunk: str):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-embedding-3-small",  # Update model if necessary
        "input": chunk
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL + embedding_endpoint, headers=headers, json=data)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from OpenAI API")

        response_data = response.json()

        # Ensure response structure matches expected format
        try:
            embedding = response_data.get("data", [{}])[0].get("embedding")
        except (IndexError, KeyError) as e:
            raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API")

        return {"embedding": embedding}
