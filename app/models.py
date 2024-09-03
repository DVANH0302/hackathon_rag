from sqlite3 import Time
from .database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from pgvector.sqlalchemy import Vector

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
    createdAt = Column(DateTime, default=None)


class Documents(Base):
    __tablename__ = "Documents"
    id = Column(Integer, primary_key = True)
