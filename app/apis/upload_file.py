from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import Dict
from io import BytesIO
from sqlalchemy.orm import Session
from ..models import DocumentEmbedding
from app.database import get_db
from datetime import datetime
from pypdf import PdfReader
from .generate_embedding import generate_embedding  # Ensure correct import

router = APIRouter()
UPLOAD_DIRECTORY = "../uploaded_files/"

def process_txt_file(contents: bytes) -> str:
    return contents.decode('utf-8')

@router.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        contents = await file.read()
        
        if file.content_type == "application/pdf":
            pdf = PdfReader(BytesIO(contents))
            chunk_size = 1000
            for page_num, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        chunks = [page_text[i:i + chunk_size] for i in range(0, len(page_text), chunk_size)]
                        for chunk in chunks:
                            embedding_response = await generate_embedding(chunk)
                            print(f"Embedding for chunk: {embedding_response}")

                            new_embedding = DocumentEmbedding(
                                file_name=file.filename,
                                content_type=file.content_type,
                                embedding=embedding_response["embedding"],  # Ensure this matches the response structure
                                created_at=datetime.now()
                            )

                            db.add(new_embedding)
                    else:
                        print(f"No text extracted from page {page_num}")
                except Exception as e:
                    print(f"Error processing page {page_num}: {e}")
                    continue

            # Commit changes after processing all pages
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error committing to the database: {e}")
                raise HTTPException(status_code=500, detail="Error saving embeddings to the database")

        elif file.content_type == "text/plain":
            # Process text files here if needed
            pass 

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing the file")
