from datetime import datetime
from sqlite3 import ProgrammingError
from sqlalchemy import ARRAY, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Text, create_engine, text
from config import POST_DB_HOST, POST_DB_NAME, POST_DB_PASS, POST_DB_PORT, POST_DB_USER
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from typing import AsyncGenerator
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

ADMIN_DATABASE_URL = f"postgresql://{POST_DB_USER}:{POST_DB_PASS}@{POST_DB_HOST}:{POST_DB_PORT}/postgres"
admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

DATABASE_URL = f"postgresql+asyncpg://{POST_DB_USER}:{POST_DB_PASS}@{POST_DB_HOST}:{POST_DB_PORT}/{POST_DB_NAME}"
Base: DeclarativeMeta = declarative_base()

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


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def create_database_if_not_exists():
    try:
        with admin_engine.connect() as conn:
            # Проверяем, существует ли база данных
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{POST_DB_NAME}'"))
            if not result.scalar():
                conn.execute(text(f"CREATE DATABASE {POST_DB_NAME}"))
                print(f"База данных {POST_DB_NAME} создана.")
            else:
                print(f"База данных {POST_DB_NAME} уже существует.")
    except ProgrammingError as e:
        raise e

async def create_db_posts():
    create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
            
    categories = [
        "Отсутствует", "Автомобили", "Бизнес", "Дом и сад", "Еда и напитки",
        "Животные", "Игры", "Искусство", "История", "Книги", "Личное развитие",
        "Мода", "Музыка", "Наука", "Образование", "Психология", "Путешествия",
        "Развлечения", "Спорт", "Технологии", "Фильмы", "Финансы", "Фотография",
        "Политика", "Здоровье"
    ]

    async with async_session_maker() as session:
        existing_categories = await session.execute(text("SELECT name FROM categories"))
        existing_categories = {row[0] for row in existing_categories.fetchall()}

        new_categories = [Category(name=name) for name in categories if name not in existing_categories]

        if new_categories:
            session.add_all(new_categories)
            await session.commit()
            print("Категории добавлены в базу данных.")
        else:
            print("Все категории уже существуют.")

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)