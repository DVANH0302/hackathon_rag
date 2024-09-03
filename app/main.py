from fastapi import FastAPI, HTTPException, Depends 
import httpx
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from .crud import *
from .models import * 
from .schemas import *
from .database import SessionLocal, engine, get_db

# load the environment variable 
load_dotenv()

# innitialize the database 
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# OpenAI API endpoint
chat_completion_endpoint = "/chat/completions"
embedding_enpoint = "/embeddings"

# Make sure to set your OpenAI API key in the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")





@app.post("/generate-response/")
async def generate_response(request: PromptRequest, db: Session = Depends(get_db)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Customize your request body based on the OpenAI API documentation
    data = {
        "model": "gpt-4",  # Replace with the appropriate model if necessary
        "messages": [{"role": "user", "content": request.prompt}],
        "max_tokens": 150  # You can adjust this according to your needs
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL+chat_completion_endpoint, headers=headers, json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from OpenAI API")

        response_data = response.json()

        db_chatSession = models.ChatSession(prompt = request.prompt, response = response_data["choices"][0]["message"]["content"])
        db.add(db_chatSession)
        db.commit()
        db.refresh(db_chatSession)

        return {"prompt": request.prompt, "response": response_data["choices"][0]["message"]["content"]}