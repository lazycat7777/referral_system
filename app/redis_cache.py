import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

# Создаем асинхронный клиент Redis
redis_client = redis.from_url(REDIS_URL)

async def get_referral_code_from_cache(key: str):
    """Возвращает реферальный код из кэша."""
    return await redis_client.get(key)

async def set_referral_code_in_cache(key: str, value: str):
    """Сохраняет реферальный код в кэш."""
    await redis_client.set(key, value)