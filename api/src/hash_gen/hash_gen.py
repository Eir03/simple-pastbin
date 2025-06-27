from fastapi import FastAPI, HTTPException
import redis
import uuid
from threading import Thread
import time
import os

# Подключение к Redis
r = redis.Redis(host=os.environ.get("HOST_REDIS"), 
                port=os.environ.get("PORT_REDIS"), 
                db=os.environ.get("DB_REDIS"),
                password=os.environ.get("REDIS_PASSWORD"))

HASH_CACHE_KEY = os.environ.get("HASH_CACHE_KEY")  # Ключ для хранения хешей
MAX_COUNT = int(os.environ.get("MAX_COUNT"))

def generate_hash():
    return str(uuid.uuid4())[10:].replace('-','')

# Функция для наполнения кэша хешами
def populate_cache():
    while True:
        if r.llen(HASH_CACHE_KEY) < MAX_COUNT:
            for _ in range(MAX_COUNT):
                r.lpush(HASH_CACHE_KEY, generate_hash()) 
        time.sleep(10)  # 10 секунд перед следующей проверкой

# Запуск фоновой задачи для наполнения кэша
# TODO: сделать через redis
Thread(target=populate_cache, daemon=True).start()


# Функция для получения хеша
async def get_hash():
    if r.llen(HASH_CACHE_KEY) == 0:  # Если кэш пуст
        return generate_hash()
    return r.rpop(HASH_CACHE_KEY).decode("utf-8")  # Возвращаем хеш из кэша
