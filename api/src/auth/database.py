import datetime
from sqlite3 import ProgrammingError
from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from .models import role
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import DeclarativeBase

from config import AUTH_DB_HOST, AUTH_DB_NAME, AUTH_DB_PASS, AUTH_DB_PORT, AUTH_DB_USER

# Административное подключение к базе данных
ADMIN_DATABASE_URL = f"postgresql+asyncpg://{AUTH_DB_USER}:{AUTH_DB_PASS}@{AUTH_DB_HOST}:{AUTH_DB_PORT}/postgres"
admin_engine = create_async_engine(ADMIN_DATABASE_URL)

DATABASE_URL = f"postgresql+asyncpg://{AUTH_DB_USER}:{AUTH_DB_PASS}@{AUTH_DB_HOST}:{AUTH_DB_PORT}/{AUTH_DB_NAME}"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.datetime.now)
    role_id = Column(Integer, nullable=True)
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_database_if_not_exists():
    async with admin_engine.connect() as conn:
        try:
            await conn.execute(f"CREATE DATABASE {AUTH_DB_NAME}")
            print(f"База данных {AUTH_DB_NAME} создана.")
        except ProgrammingError as e:
            if "already exists" in str(e):
                print(f"База данных {AUTH_DB_NAME} уже существует.")
            else:
                raise


async def create_db_and_tables():
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

