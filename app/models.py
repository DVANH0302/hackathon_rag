from .database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from pgvector.sqlalchemy import Vector
from datetime import datetime


# class ChatSession(Base):
#     __tablename__ = "chatSession"
#     id = Column(Integer, primary_key = True)
#     Content = Column(String)
#     embedding = Column(Vector(dim = 512)) 


class ChatSession(Base):
    __tablename__ = "ChatSession"
    id = Column(Integer, primary_key = True)
    prompt = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # Assuming a 1536-dimensional vector (e.g., from OpenAI)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<DocumentEmbedding(file_name={self.file_name}, id={self.id})>"