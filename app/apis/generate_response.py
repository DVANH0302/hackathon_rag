# app/apis/generate_response.py
from fastapi import APIRouter, HTTPException, Depends
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from app.crud import *
from app.models import ChatSession
from app.schemas import PromptRequest
from app.database import get_db

# Load environment variables
load_dotenv()

# OpenAI API configuration
chat_completion_endpoint = "/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

router = APIRouter()

@router.post("/generate-response/")
async def generate_response(request: PromptRequest, db: Session = Depends(get_db)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",  # Replace with the appropriate model if necessary
        "messages": [{"role": "user", "content": request.prompt}],
        "max_tokens": 150  # You can adjust this according to your needs
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL + chat_completion_endpoint, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from OpenAI API")

        response_data = response.json()

        db_chatSession = ChatSession(prompt=request.prompt, response=response_data["choices"][0]["message"]["content"])
        db.add(db_chatSession)
        db.commit()
        db.refresh(db_chatSession)

        return {"prompt": request.prompt, "response": response_data["choices"][0]["message"]["content"]}
