import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.from_url(REDIS_URL)


async def get_referral_code_from_cache(key: str):
    """Возвращает реферальный код из кэша."""
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Redis error: {e}")
        return None


async def set_referral_code_in_cache(key: str, value: str):
    """Сохраняет реферальный код в кэш."""
    try:
        await redis_client.set(key, value)
    except Exception as e:
        print(f"Redis error: {e}")


async def delete_referral_code_from_cache(code: str):
    """Удаляет реферальный код из кэша."""
    try:
        await redis_client.delete(code)
    except Exception as e:
        print(f"Redis error: {e}")
