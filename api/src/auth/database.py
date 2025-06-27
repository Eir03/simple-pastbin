import datetime
from fastapi import Depends
from sqlalchemy import TIMESTAMP, Column, Integer, String, text, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Role


async def init_roles(session: AsyncSession):
    """Инициализация ролей пользователей"""
    default_roles = [
        {
            "id": 1, 
            "name": "user",            
        },
        {
            "id": 2, 
            "name": "admin",
        }
    ]

    for role_data in default_roles:
        existing_role = await session.get(Role, role_data["id"])
        
        if not existing_role:
            role = Role(
                id=role_data["id"],
                name=role_data["name"],
            )
            session.add(role)
            print(f"Создана роль: {role_data['name']}")
    
    await session.commit()
    print("Инициализация ролей завершена")

