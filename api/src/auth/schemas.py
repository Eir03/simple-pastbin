from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class RoleBase(BaseModel):
    """Базовая схема для роли"""
    name: str
    permissions: Optional[List[str]] = None


class RoleCreate(RoleBase):
    """Схема для создания роли"""
    pass


class RoleUpdate(RoleBase):
    """Схема для обновления роли"""
    name: Optional[str] = None


class Role(RoleBase):
    """Схема для получения роли"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Базовая схема для пользователя"""
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов")
    password_confirm: str = Field(..., description="Подтверждение пароля")
    role_id: Optional[int] = 1  # По умолчанию роль обычного пользователя


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role_id: Optional[int] = None


class User(UserBase):
    """Схема для получения пользователя"""
    id: int
    registered_at: datetime
    role_id: int
    role: Optional[Role] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=8)


class Token(BaseModel):
    """Схема для токена доступа"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    """Схема для данных в токене"""
    sub: str  # user_id
    exp: datetime
    type: str = "access"  # access или refresh


class RefreshToken(BaseModel):
    """Схема для обновления токена"""
    refresh_token: str


class PasswordReset(BaseModel):
    """Схема для сброса пароля"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Схема для подтверждения сброса пароля"""
    token: str
    new_password: str = Field(..., min_length=8)
    new_password_confirm: str