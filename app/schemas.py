from pydantic import BaseModel 

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str



class PromptRequest(BaseModel):
    prompt: str


class FileCreate(BaseModel):
    file_name: str
    content_type: str

