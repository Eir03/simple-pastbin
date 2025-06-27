from dotenv import load_dotenv
import os

from pydantic import BaseModel

load_dotenv()

POST_DB_HOST = os.environ.get("POSTGRES_HOST")
POST_DB_PORT = os.environ.get("POSTGRES_PORT")
POST_DB_NAME = os.environ.get("POSTGRES_DB")
POST_DB_USER = os.environ.get("POSTGRES_USER")
POST_DB_PASS = os.environ.get("POSTGRES_PASSWORD")

USE_BLOB = os.getenv('USE_BLOB', 'false').lower() == 'true'
URL_BLOB = os.environ.get("URL_BLOB")
BLOB_ACCESS_KEY = os.getenv('BLOB_ACCESS_KEY')
BLOB_SECRET_KEY = os.getenv('BLOB_SECRET_KEY')
BLOB_SECURE = os.getenv('BLOB_SECURE', 'false').lower() == 'true'
BUCKET = os.getenv('BUCKET')


class AuthConfig(BaseModel):
    """Конфигурация для аутентификации"""
    PRIVATE_KEY_PATH: str = "/app/keys/private.pem"
    PUBLIC_KEY_PATH: str = "/app/keys/public.pem"
    ALGORITHM: str = "RS256"

    @property
    def private_key(self):
        with open(self.PRIVATE_KEY_PATH, "r") as f:
            return f.read()

    @property
    def public_key(self):
        with open(self.PUBLIC_KEY_PATH, "r") as f:
            return f.read()

# Создаем экземпляр конфигурации
auth_config = AuthConfig()
