from fastapi import FastAPI
# from .routers import generate_embedding, generate_response, upload_file

from app.routers.apis import router as router 
from .database import engine, SessionLocal
from . import models
from .config import OPENAI_API_KEY


from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings



# init open api key, llm, embedding for llamaIndex:
Settings.openai_api_key = OPENAI_API_KEY
Settings.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
Settings.embed_model= OpenAIEmbedding(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


@app.get('/')
async def root():
    return {"message": 'Hello world'}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8080)