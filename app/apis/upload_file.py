from fastapi import APIRouter, UploadFile, File
from typing import Dict
from io import BytesIO
# from docx import Document
from pypdf import PdfReader

router = APIRouter()

def read_txt_file(contents: bytes) -> str:
    return contents.decode('utf-8')

# def read_docx_file(file: BytesIO) -> str:
#     doc = Document(file)
#     text = []
#     for para in doc.paragraphs:
#         text.append(para.text)
#     return "\n".join(text)


@router.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        # Read the content of the uploaded file
        contents = await file.read()
        file_stream = BytesIO(contents)
        
        # Determine file type and read accordingly
        if file.filename.endswith('.txt'):
            file_content = read_txt_file(contents)
        # elif file.filename.endswith('.docx'):
        #     file_content = read_docx_file(file_stream)
        elif file.filename.endswith('.pdf'):
            reader = PdfReader(BytesIO(contents))
            file_content = "\n".join([page.extract_text() for page in reader.pages])
        else:
            return {"message": "Unsupported file type"}

    except Exception as e:
        # Log or print the exception for debugging
        print(f"An error occurred: {e}")
        return {"message": "There was an error processing the file"}
    
    finally:
        # Ensure the uploaded file stream is closed
        await file.close()

    # Return the content of the file
    return {"message": f"Successfully processed {file.filename}", "content": file_content}
