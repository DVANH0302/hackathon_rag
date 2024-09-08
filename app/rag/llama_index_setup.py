from ..config import DB_HOST,DB_NAME,DB_PASSWORD,DB_PORT, DB_USERNAME, OPENAI_API_KEY       
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core import VectorStoreIndex, Settings
Settings.openai_api_key = OPENAI_API_KEY


def get_vector_store():
    vector_store = PGVectorStore.from_params(
    database=DB_NAME,
    host=DB_HOST,
    password=DB_PASSWORD,
    port=DB_PORT,
    user=DB_USERNAME,
    table_name="vector",
    embed_dim=1536,  # openai embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
    # hybrid_search=True,
    # text_search_config="english"
)

    return vector_store

def initialize_llamaindex():
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7)

    vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(vector_store, llm = llm)

    # retriever = index.as_retriever(limit=2,
    #     rerank={
    #     "model": "mixedbread-ai/mxbai-rerank-base-v1",
    #     "num_documents_to_rerank": 100
    # })
    # docs = retriever.retrieve("What did the author do as a child?")
    # for doc in docs:
    #     print("---------")
    #     print(f"Id: {doc.id_}")
    #     print(f"Score: {doc.score}")
    #     print(f"Text: {doc.text}")

    standard_query_engine = index.as_query_engine(
        # streaming  = True,
        # vector_search_limit = 20, 
        # vector_search_rerank = {
        #     "model": "mixedbread-ai/mxbai-rerank-base-v1",
        #     "num_documents_to_rerank": 100,
        # }
    )

    return standard_query_engine