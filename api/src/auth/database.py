import datetime
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, get_async_session

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

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def init_roles(session: AsyncSession):
    """Инициализация ролей пользователей"""
    roles = [
        {"id": 1, "name": "user"},
        {"id": 2, "name": "admin"}
    ]

    for role in roles:
        result = await session.execute(
            text("SELECT 1 FROM roles WHERE id = :id"),
            {"id": role["id"]}
        )
        if not result.scalar():
            await session.execute(
                text("INSERT INTO roles (id, name) VALUES (:id, :name)"),
                role
            )
    
    await session.commit()

