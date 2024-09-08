from fastapi import FastAPI
# from .routers import generate_embedding, generate_response, upload_file

from app.routers.generate_response import router as generate_response_router
from app.routers.upload_file import router as upload_file_router
from app.routers.generate_embedding import router as generate_embedding_router
from app.routers.query import router as query_router
from .database import engine, SessionLocal
from . import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(query_router)
app.include_router(generate_response_router)
app.include_router(upload_file_router)
app.include_router(generate_embedding_router)

@app.get('/')
async def root():
    return {"message": 'Hello world'}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8080)