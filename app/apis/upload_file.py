from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import Dict
from io import BytesIO
from sqlalchemy.orm import Session
from ..models import Documents
import os
from pypdf import PdfReader
from app.database import get_db
from datetime import datetime

router = APIRouter()

UPLOAD_DIRECTORY = "../uploaded_files/"

def read_txt_file(contents: bytes) -> str:
    return contents.decode('utf-8')

def read_pdf_file(file: BytesIO) -> str:
    text = []
    pdf = PdfReader(file)
    for page in pdf.pages:
        text.append(page.extract_text())
    return "\n".join(text)

# def read_docx_file(file: BytesIO) -> str:
#     doc = Document(file)
#     text = []
#     for para in doc.paragraphs:
#         text.append(para.text)
#     return "\n".join(text)

@router.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:


        # Save the file to the filesystem
        contents = await file.read()
        
        # Read file content based on file type
        if file.content_type == "application/pdf":
            file_text = read_pdf_file(BytesIO(contents))
        elif file.content_type == "text/plain":
            file_text = read_txt_file(contents)
        # elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        #     file_text = read_docx_file(BytesIO(contents))
        else:
            file_text = None  # Or handle other file types

        new_document = Documents(
            file_name = file.filename,
            content = file_text
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        return {"filename": new_document.file_name,  "content": file_text}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing the file")
