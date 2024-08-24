from fastapi import FastAPI, HTTPException
import redis
import uuid
from threading import Thread
import time

app = FastAPI(description="hash generator")

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

HASH_CACHE_KEY = "hash_cache"  # Ключ для хранения хешей в кэше

# Функция генерации хеша
def generate_hash():
    return str(uuid.uuid4())[10:].replace('-','')

# Функция для наполнения кэша хешами
def populate_cache():
    while True:
        print(f"Количество хешей =",r.llen(HASH_CACHE_KEY))
        if r.llen(HASH_CACHE_KEY) < 1000:  # Если в кэше меньше 1000 хешей
            for _ in range(1000):
                r.lpush(HASH_CACHE_KEY, generate_hash())  # Добавляем новые хеши в кэш
        time.sleep(10)  # Спим 10 секунд перед следующей проверкой

# Запуск фоновой задачи для наполнения кэша, потом будет через celery
Thread(target=populate_cache, daemon=True).start()



# Endpoint для получения хеша
@app.get("/get-hash")
async def get_hash():
    if r.llen(HASH_CACHE_KEY) == 0:  # Если кэш пуст
        # print('Без кеша')
        return {"hash": generate_hash()}
    # print('C кешом')
    return {"hash": r.rpop(HASH_CACHE_KEY).decode("utf-8")}  # Возвращаем хеш из кэша
