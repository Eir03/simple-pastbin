from dotenv import load_dotenv
import os

load_dotenv()

AUTH_DB_HOST = os.environ.get("AUTH_DB_HOST")
AUTH_DB_PORT = os.environ.get("AUTH_DB_PORT")
AUTH_DB_NAME = os.environ.get("AUTH_DB_NAME")
AUTH_DB_USER = os.environ.get("AUTH_DB_USER")
AUTH_DB_PASS = os.environ.get("AUTH_DB_PASS")

AUTH_SECRET = os.environ.get("AUTH_SECRET")
AUTH_PASS_SECRET = os.environ.get("AUTH_PASS_SECRET")

POST_DB_HOST = os.environ.get("POST_DB_HOST")
POST_DB_PORT = os.environ.get("POST_DB_PORT")
POST_DB_NAME = os.environ.get("POST_DB_NAME")
POST_DB_USER = os.environ.get("POST_DB_USER")
POST_DB_PASS = os.environ.get("POST_DB_PASS")

USE_BLOB= os.getenv('USE_BLOB')
URL_BLOB = os.environ.get("URL_BLOB")
BLOB_ACCESS_KEY = os.getenv('BLOB_ACCESS_KEY')
BLOB_SECRET_KEY = os.getenv('BLOB_SECRET_KEY')
BLOB_SECURE = os.getenv('BLOB_SECURE')
BUCKET = os.getenv('BUCKET')