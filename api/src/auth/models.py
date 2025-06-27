from datetime import datetime
from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


# TODO: Добавить permissions
class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    permissions = Column(JSON, nullable=True)
    

    users = relationship("User", back_populates="role")

    def __str__(self):
        return self.name

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.now)
    role_id = Column(Integer, ForeignKey('role.id'))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    

    role = relationship("Role", back_populates="users")
    posts = relationship("Post", back_populates="user")

    def has_permission(self, permission: str) -> bool:
        """Проверка наличия права у пользователя"""
        if self.is_superuser:
            return True
        if self.role and self.role.permissions:
            return permission in self.role.permissions
        return False

    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        from .utils import verify_password
        return verify_password(password, self.hashed_password)

    @property
    def is_authenticated(self) -> bool:
        """Проверка аутентификации пользователя"""
        return True if self.id else False

    def __str__(self):
        return f"{self.username} ({self.email})"