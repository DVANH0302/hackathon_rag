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


class Documents(Base):
    __tablename__ = "Documents"
    id = Column(Integer, primary_key = True)
    file_name = Column(String)
    content  = Column(String)

 