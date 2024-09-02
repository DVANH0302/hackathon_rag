from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from pgvector.sqlalchemy import Vector
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_sessions")

class StudyMaterial(Base):
    __tablename__ = 'study_materials'

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    content = Column(BYTEA)

    chat_session = relationship("ChatSession", back_populates="study_materials")

class MessageEmbedding(Base):
    __tablename__ = 'message_embeddings'

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    content = Column(Text)
    embedding = Column(Vector(1536))  # Example with a 1536-dimensional vector

    chat_session = relationship("ChatSession", back_populates="message_embeddings")
