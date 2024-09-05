from fastapi import FastAPI

from .crud import *
from .models import * 
from .schemas import *
from .database import SessionLocal, engine, get_db
from app.apis import upload_file, generate_response, generate_embedding


# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(upload_file.router)
app.include_router(generate_response.router)
app.include_router(generate_embedding.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
