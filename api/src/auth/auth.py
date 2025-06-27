from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from .utils import verify_password, get_password_hash, create_token, verify_token
from .models import User
from .schemas import UserLogin, UserCreate, Token, RefreshToken
from sqlalchemy import select
from datetime import datetime

router_auth = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router_auth.post('/register', response_model=Token)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Регистрация нового пользователя"""
    # Проверяем, что пароли совпадают
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )
    
    # Проверяем, что пользователь с таким email не существует
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        role_id=user_data.role_id,
        registered_at=datetime.utcnow()
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    # Создаем токены
    access_token = create_token(str(new_user.id), "access")
    refresh_token = create_token(str(new_user.id), "refresh")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router_auth.post('/login', response_model=Token)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """Вход пользователя"""
    # Ищем пользователя по email
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Создаем токены
    access_token = create_token(str(user.id), "access")
    refresh_token = create_token(str(user.id), "refresh")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router_auth.post('/refresh', response_model=Token)
async def refresh_token(
    token_data: RefreshToken,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление токена доступа"""
    # Проверяем refresh token
    payload = verify_token(token_data.refresh_token, "refresh")
    
    # Получаем пользователя
    query = select(User).where(User.id == int(payload["sub"]))
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    # Создаем новые токены
    access_token = create_token(str(user.id), "access")
    refresh_token = create_token(str(user.id), "refresh")
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )