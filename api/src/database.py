from sqlite3 import ProgrammingError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from typing import AsyncGenerator
from config import POST_DB_HOST, POST_DB_NAME, POST_DB_PASS, POST_DB_PORT, POST_DB_USER


Base: DeclarativeMeta = declarative_base()

# URL для административного доступа
ADMIN_DATABASE_URL = f"postgresql://{POST_DB_USER}:{POST_DB_PASS}@{POST_DB_HOST}:{POST_DB_PORT}/postgres"
admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")


DATABASE_URL = f"postgresql+asyncpg://{POST_DB_USER}:{POST_DB_PASS}@{POST_DB_HOST}:{POST_DB_PORT}/{POST_DB_NAME}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def create_database_if_not_exists():
    """Создает базу данных, если она не существует"""
    try:
        with admin_engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{POST_DB_NAME}'"))
            if not result.scalar():
                conn.execute(text(f"CREATE DATABASE {POST_DB_NAME}"))
                print(f"База данных {POST_DB_NAME} создана.")
            else:
                print(f"База данных {POST_DB_NAME} уже существует.")
    except ProgrammingError as e:
        raise e

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронных сессий для работы с БД"""
    async with async_session_maker() as session:
        yield session

async def init_db():
    """Инициализация базы данных"""
    create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)