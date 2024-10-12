from fastapi import FastAPI, HTTPException
import redis
import uuid
from threading import Thread
import time
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_DB_HOST = os.environ.get("AUTH_DB_HOST")
app = FastAPI(description="hash generator")

# Подключение к Redis
r = redis.Redis(os.environ.get("HOST_REDIS"), 
                port=os.environ.get("PORT_REDIS"), 
                db=os.environ.get("DB_REDIS"))

HASH_CACHE_KEY = os.environ.get("HASH_CACHE_KEY")  # Ключ для хранения хешей в кэше
MAX_COUNT = os.environ.get("MAX_COUNT")

def generate_hash():
    return str(uuid.uuid4())[10:].replace('-','')

# Функция для наполнения кэша хешами
def populate_cache():
    while True:
        if r.llen(HASH_CACHE_KEY) < MAX_COUNT:
            for _ in range(MAX_COUNT):
                r.lpush(HASH_CACHE_KEY, generate_hash()) 
        time.sleep(10)  # Спим 10 секунд перед следующей проверкой

# Запуск фоновой задачи для наполнения кэша, потом будет через celery
Thread(target=populate_cache, daemon=True).start()


# Endpoint для получения хеша
@app.get("/get-hash")
async def get_hash():
    if r.llen(HASH_CACHE_KEY) == 0:  # Если кэш пуст
        return {"hash": generate_hash()}
    return {"hash": r.rpop(HASH_CACHE_KEY).decode("utf-8")}  # Возвращаем хеш из кэша
