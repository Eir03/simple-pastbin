from datetime import datetime
from sqlite3 import ProgrammingError
from sqlalchemy import ARRAY, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Text, create_engine, text
from api.src.database import Base
from config import POST_DB_HOST, POST_DB_NAME, POST_DB_PASS, POST_DB_PORT, POST_DB_USER
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from typing import AsyncGenerator
from sqlalchemy.orm import relationship
from sqlalchemy.future import select


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True) 
    category_id = Column(Integer, ForeignKey('categories.id'), default=1)
    title = Column(String, index=True, nullable=True)
    hash = Column(String, unique=True, nullable=False)
    blob_storage_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_public = Column(Boolean, default=True)
    delete_after_reading = Column(Boolean, default=False)
    tags = Column(ARRAY(String), nullable=True)
    category = relationship("Category")
    content = Column(String, nullable=True)


