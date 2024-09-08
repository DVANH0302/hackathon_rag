from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import Dict
from io import BytesIO
from sqlalchemy.orm import Session
from ..models import DocumentEmbedding
from app.database import get_db
from datetime import datetime
from pypdf import PdfReader
from .generate_embedding import generate_embedding  
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.text_splitter import TokenTextSplitter
import json
import openai
from ..config import OPENAI_API_KEY
from app.rag.llama_index_setup import get_vector_store

openai.api_key = OPENAI_API_KEY



router = APIRouter()

def chunk_text(text, chunk_size=512, chunk_overlap=20):
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

@router.post("/upload-file/")
async def create_upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    chunk_size: int = 512,
    chunk_overlap: int = 20
):
    if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        contents = await file.read()
        
        document_embedding = DocumentEmbedding(file_name = file.filename, content_type = file.content_type)
        db.add(document_embedding)
        db.flush()
        db.commit()

        try: 
            vector_store = get_vector_store()
            storage_context = StorageContext.from_defaults(vector_store = vector_store)
        except Exception as e:
            print("vector_store", e)

        chunks_created = 0
        if file.content_type == "application/pdf":
            pdf = PdfReader(BytesIO(contents))
            documents = []
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    chunks = chunk_text(page_text)
                    chunks_created += len(chunks)
                
                for chunk in chunks:
                    document = Document(
                        text = chunk, 
                        metadata = {
                            "file_name": file.filename,
                            "content_type": file.content_type,
                            "document_id_foreign_key": document_embedding.id,   
                            "page_number": page_num + 1,
                        }
                    )
                    documents.append(document)

            index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context,
            show_progress=True
        )
                

        elif file.content_type == "text/plain":
            full_text = contents.decode('utf-8') 

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing the file")

    return {"result": "Upload Done"}


# from llama_index.core import SimpleDirectoryReader, StorageContext
# from llama_index.core import VectorStoreIndex
# from llama_index.vector_stores.postgres import PGVectorStore
# import textwrap
# import openai
# from ..config import OPENAI_API_KEY
# # from ..config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME, AWS_S3_REGION_NAME
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from ..database import get_db
# from sqlalchemy.orm import Session


# # import logging
# # import boto3
# # from botocore.exceptions import ClientError
# # import os
# # # Initialize S3 client
# # s3_client = boto3.client(
# #     's3',
# #     region_name=AWS_S3_REGION_NAME,
# #     aws_access_key_id=AWS_ACCESS_KEY_ID,
# #     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# # )


# router = APIRouter()


# @router.post("/upload-file/")
# async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         documents = SimpleDirectoryReader(file).load_data()
#         print("Document ID:", documents[0].doc_id)
#     except Exception as e: 
#         print(f"Error loading data from file: {e}")


