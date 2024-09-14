import os
import logging
from typing import Dict, List
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from ..config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME, OPENAI_API_KEY

from llama_index.core import (
    VectorStoreIndex, 
    StorageContext, 
    SimpleDirectoryReader, 
    Settings, 
    SummaryIndex
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.agent.openai import OpenAIAgent
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Adjust level as needed

load_dotenv()

UPLOAD_DIR = r".\app\uploaded_data"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)







def get_vector_store(table_name: str) -> PGVectorStore:
    try:
        return PGVectorStore.from_params(
            database=DB_NAME,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
            user=DB_USERNAME,
            table_name=table_name,
            embed_dim=1536,
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
            },
        )
    except Exception as e:
        logger.error(f"Failed to create vector store: {e}")
        raise

def load_file_first_time(file_path:str, file_name:str):
    try:
        vector_store = get_vector_store(table_name=f"{file_name[:-4]}_vector")
        storage_context = StorageContext.from_defaults(vector_store=vector_store) 
        docs = SimpleDirectoryReader(input_files=[file_path]).load_data()
        node_parser = SentenceSplitter()
        nodes = node_parser.get_nodes_from_documents(docs)
        vector_index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
        )
        print(f"Created new VectorStoreIndex for {file_name}") 

    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")
        return None


def retrieve_tool(file_name: str) -> Dict:
    try:
        # print(f"{file_name[:-4]}_vector")
        vector_store = get_vector_store(table_name=f"{file_name[:-4]}_vector")
        vector_index = VectorStoreIndex.from_vector_store(vector_store = vector_store)
        # nodes = vector_index.docstore.docs.values()
        # print("nodes:", nodes)
        # summary_index = SummaryIndex(nodes)
        print(f"Loaded existing VectorStoreIndex for {file_name}")

        
        vector_query_engine = vector_index.as_query_engine(
        similarity_top_k=2,

        )
        
        vector_tool = QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name=f"vector_tool_{file_name[:-4]}",
                description=f"Use this tool if you have specific questions over {file_name}",
            ),
        )

        # summary_query_engine = summary_index.as_query_engine(
        #         response_mode="tree_summarize",
        #         use_async=True,
        #     )        
        summary_query_engine = vector_index.as_query_engine(
                response_mode="tree_summarize",
                use_async=True,
            )

        summary_tool = QueryEngineTool.from_defaults(
            name=f"summary_tool_{file_name[:-4]}",
            query_engine=summary_query_engine,
            description=(
                f"Use ONLY IF you want to get a holistic summary of {file_name}. "
                f"Do NOT use if you have specific questions over {file_name}."
            ),
        )

        
        return {"vector_tool":vector_tool, "summary_tool": summary_tool}
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")
        return None

def build_agent(upload_dir: str = UPLOAD_DIR) -> OpenAIAgent:
    files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
    # print(files)
    documents_to_tools_dict = {}

    for file_name in files:
        result = retrieve_tool(file_name)
        if result:
            vector_tool = result['vector_tool']
            summary_tool = result['summary_tool']
        documents_to_tools_dict[file_name]= [vector_tool, summary_tool]
    initial_tools = [t for file_name in files for t in documents_to_tools_dict[file_name]]
    if not initial_tools:
        logger.error("No tools created. Check if files are present and readable.")
        raise ValueError("No tools created")
    
    ##################
    llm= OpenAI(api_key=OPENAI_API_KEY,model='gpt-3.5-turbo')
    ####################
    agent_worker= FunctionCallingAgentWorker.from_tools(
        initial_tools,
        llm=llm,
        verbose=True,
    )
    agent= AgentRunner(agent_worker)
    return agent



# Main execution
if __name__ == "__main__":
    try:
        agent = build_agent()
        response = agent.query(
        "Tell me about the evaluation dataset used in LongLoRA, "
        "and then tell me about the evaluation results"
    )
        print(response)
    except Exception as e:
        logger.error(f"An error occurred: {e}") 


