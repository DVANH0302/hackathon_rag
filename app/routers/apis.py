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




@router.get("/file/", response_model=schemas.File)
def read_file(name:str, db:Session = Depends(get_db)):
    file = crud.get_filename(db, file_name = name)
    if file is None:
        return False
    return True

@router.post("/upload-file/", response_model = schemas.File)
async def create_upload_file(
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db),
    background_task: BackgroundTasks = None
):
    ## ADD document info to document table 
    uploaded_files = []

            

    for file in files: 
        try:
            if not file.content_type.startswith("text/") and not file.content_type.startswith("application/"):
                raise HTTPException(status_code=400, detail="Unsupported file type")

            file_exists = read_file(name=file.filename, db = db)
            if not file_exists:
                background_tasks.add_task(load_file_first_time, file_path, file.filename)



            contents = await file.read()
            file_path = os.path.join(upload_dir, file.filename) 
            print(f"Saving file to: {file_path}")       
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(contents)
            
            # save file info to database
            document = schemas.File(file_name = file.file_name, content_type = file.content_type)
            db_file = crud.add_document(db = db, file = file_create)
            uploaded_files.append(db_file)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="There was an error processing the file")
        finally:
            await file.close()        

    

    return {"result": "Upload Done", "files": uploaded_files}

#######################################################
# from dotenv import load_dotenv
# from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Settings, SummaryIndex
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.llms.openai import OpenAI
# from llama_index.vector_stores.postgres import PGVectorStore
# from llama_index.core.tools import QueryEngineTool, ToolMetadata
# from llama_index.agent.openai import OpenAIAgent
# from llama_index.core.vector_stores import MetadataFilters, FilterCondition
# from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
# from llama_index.llms.openai import OpenAI
# import os
# import logging
# from typing import Dict, List
# from dotenv import load_dotenv
# from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# load_dotenv()

# # Configuration
# DATABASE_URL = os.getenv("DATABASE_URL")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_URL = os.getenv("OPENAI_API_URL")
# DB_USERNAME = os.getenv('DB_USERNAME')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')
# def get_vector_store(table_name: str) -> PGVectorStore:
#     try:
#         return PGVectorStore.from_params(
#             database=DB_NAME,
#             host=DB_HOST,
#             password=DB_PASSWORD,
#             port=DB_PORT,
#             user=DB_USERNAME,
#             table_name=table_name,
#             embed_dim=1536,
#             hnsw_kwargs={
#                 "hnsw_m": 16,
#                 "hnsw_ef_construction": 64,
#                 "hnsw_ef_search": 40,
#                 "hnsw_dist_method": "vector_cosine_ops",
#             },
#         )
#     except Exception as e:
#         logger.error(f"Failed to create vector store: {e}")
#         raise

# def load_file_first_time(file_path:str, file_name:str):
#     try:
#         vector_store = get_vector_store(table_name=f"{file_name[:-4]}_vector")
#         storage_context = StorageContext.from_defaults(vector_store=vector_store) 
#         docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
#         node_parser = SentenceSplitter()
#         nodes = node_parser.get_nodes_from_documents(docs)
#         vector_index = VectorStoreIndex(
#             nodes,
#             storage_context=storage_context,
#         )
#         print(f"Created new VectorStoreIndex for {file_name}") 

#     except Exception as e:
#         logger.error(f"Error processing file {file_name}: {e}")
#         return None


# def retrieve_tool(file_name: str) -> Dict:
#     try:
#         vector_store = get_vector_store(table_name=f"{file_name[:-4]}_vector")
#         storage_context = StorageContext.from_defaults(vector_store=vector_store) 
#         vector_index = VectorStoreIndex.from_vector_store(vector_store = vector_store)
#         nodes = vector_index.docstore.docs.values()
#         summary_index = SummaryIndex(nodes)
#         print(f"Loaded existing VectorStoreIndex for {file_name}")

        
#         vector_query_engine = vector_index.as_query_engine(
#         similarity_top_k=2,
#         # filters=MetadataFilters.from_dicts(
#         #         metadata_dicts,
#         #         condition=FilterCondition.OR
#         #     )
#         )
        
#         vector_tool = QueryEngineTool(
#             query_engine=vector_query_engine,
#             metadata=ToolMetadata(
#                 name=f"vector_tool_{file_name[:-4]}",
#                 description=f"Use this tool for questions about {file_name}",
#             ),
#         )

#         summary_query_engine = summary_index.as_query_engine(
#                 response_mode="tree_summarize",
#                 use_async=True,
#             )
#         summary_tool = QueryEngineTool.from_defaults(
#             name=f"summary_tool_{file_name[:-4]}",
#             query_engine=summary_query_engine,
#             description=(
#                 f"Use ONLY IF you want to get a holistic summary of {file_name}. "
#                 f"Do NOT use if you have specific questions over {file_name}."
#             ),
#         )

        
#         return {"vector_tool":vector_tool, "summary_tool": summary_tool}
#     except Exception as e:
#         logger.error(f"Error processing file {file_name}: {e}")
#         return None

# def build_agent(upload_dir: str = UPLOAD_DIR) -> OpenAIAgent:
#     files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
#     print(files)
#     documents_to_tools_dict = {}

#     for file_name in files:
#         result = retrieve_tool(file_name)
#         if result:
#             vector_tool = result['vector_tool']
#             summary_tool = result['summary_tool']
#         documents_to_tools_dict[file_name]= [vector_tool, summary_tool]
#     initial_tools = [t for file_name in files for t in documents_to_tools_dict[file_name]]
#     if not initial_tools:
#         logger.error("No tools created. Check if files are present and readable.")
#         raise ValueError("No tools created")
    
#     llm= OpenAI(api_key=OPENAI_API_KEY,model='gpt-3.5-turbo')

#     agent_worker= FunctionCallingAgentWorker.from_tools(
#         initial_tools,
#         llm=llm,
#         verbose=True
#     )
#     agent= AgentRunner(agent_worker)
#     return agent


def get_agent():
    agent = build_agent() 
    return agent

@router.post("/query/")
def query():
    agent = get_agent()
    response = agent.query(
        "Tell me about the evaluation dataset used in LongLoRA, "
        "and then tell me about the evaluation results"
    )
    return response

