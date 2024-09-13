from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import DocumentEmbedding
from app.database import get_db
from datetime import datetime
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Settings
from ..config import OPENAI_API_KEY
from .. import crud, schemas
import aiofiles
import os
from typing import List
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from app.rag.llama_index_setup import get_vector_store, load_file_first_time, retrieve_tool, build_agent
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner



# # init open api key, llm, embedding for llamaIndex:
# Settings.openai_api_key = OPENAI_API_KEY
# Settings.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
# Settings.embed_model= OpenAIEmbedding(api_key=OPENAI_API_KEY, model="text-embedding-3-small")




# Router
router = APIRouter()


# variable for upload-file api
UPLOAD_DIR = r".\app\uploaded_data"
upload_dir = r".\app\uploaded_data"
os.makedirs(upload_dir, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)




@router.get("/file/", response_model=schemas.FileCreate)
def read_file(name:str, db:Session = Depends(get_db)):
    file = crud.get_filename(db, file_name = name)
    if file is None:
        return False
    return True

@router.post("/upload-file/", response_model=List[schemas.FileCreate])
async def create_upload_file(
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db),
    background_task: BackgroundTasks = None
):
    uploaded_files = []

    for file in files: 
        try:
            if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
                raise HTTPException(status_code=400, detail="Unsupported file type")

            contents = await file.read()
            file_path = os.path.join(upload_dir, file.filename)
            print(f"Saving file to: {file_path}")       
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(contents)
            
            file_exists = read_file(name=file.filename, db=db)
            if not file_exists:
                load_file_first_time(os.path.join(upload_dir, file.filename), file.filename)
        
            # save file info to database
            document = schemas.FileCreate(file_name=file.filename, content_type=file.content_type)
            db_file = crud.add_document(db=db, file=document)
            uploaded_files.append(db_file)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="There was an error processing the file")
        finally:
            await file.close()

    return uploaded_files


# @router.post("/upload-file/", response_model = schemas.FileCreate)
# async def create_upload_file(
#     files: List[UploadFile] = File(...), 
#     db: Session = Depends(get_db),
#     background_task: BackgroundTasks = None
# ):
#     ## ADD document info to document table 
#     uploaded_files = []

            

#     for file in files: 
#         try:
#             if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
#                 raise HTTPException(status_code=400, detail="Unsupported file type")


#             contents = await file.read()
#             file_path = os.path.join(upload_dir, file.filename) 
#             print(f"Saving file to: {file_path}")       
#             async with aiofiles.open(file_path, 'wb') as f:
#                 await f.write(contents)
            
#             file_exists = read_file(name=file.filename, db = db)
#             if not file_exists:
#                 load_file_first_time(os.path.join(upload_dir, file.filename),file.filename)
           
#             # save file info to database
#             document = schemas.FileCreate(file_name = file.filename, content_type = file.content_type)
#             db_file = crud.add_document(db = db, file = document)
#             uploaded_files.append(db_file)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             raise HTTPException(status_code=500, detail="There was an error processing the file")
#         finally:
#             await file.close()        

    

#     return True



@router.post("/query/")
def query(request: str ):
    agent = build_agent()
    response = agent.query(request)
    return response

