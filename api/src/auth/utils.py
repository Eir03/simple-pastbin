from datetime import datetime, timezone, timedelta
import jwt
from config import auth_config
from passlib.context import CryptContext
from fastapi import HTTPException, status
from typing import Optional

def encode_jwt(payload: dict, 
               private_key: str = auth_config.private_key, 
               algorithm: str = auth_config.ALGORITHM):
    
    to_encode = payload.copy()
    to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=15)})
    to_encode.update({'iat': datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, key=private_key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(token: str | bytes, 
               public_key: str = auth_config.public_key, 
               algorithm: str = auth_config.ALGORITHM):
    decoded_jwt = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)

def create_token(user_id: str, token_type: str = "access") -> str:
    """Создание JWT токена"""
    expire_delta = timedelta(minutes=15) if token_type == "access" else timedelta(days=7)
    expire = datetime.now(timezone.utc) + expire_delta
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type,
        "iat": datetime.now(timezone.utc)
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        auth_config.private_key,
        algorithm=auth_config.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str, token_type: Optional[str] = None) -> dict:
    """Проверка JWT токена"""
    try:
        payload = jwt.decode(
            token,
            auth_config.public_key,
            algorithms=[auth_config.ALGORITHM]
        )
        
        # Проверяем тип токена, если указан
        if token_type and payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена"
            )
            
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истек"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )