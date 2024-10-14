from redis import asyncio as aioredis
from config import REDIS_HOST, REDIS_PORT
import uuid
import time

redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

async def create_new_session(username: str, ttl: int = 3600):
    sid = str(uuid.uuid4())
    await redis.setex(f"session:{sid}", ttl, username)

    expiration_timestamp = time.time() + ttl

    return {"session_id": sid, 
            "expire_time": expiration_timestamp}

async def validate_session(sid: str):
    return await redis.get(f"session:{sid}")

async def renew_session(sid: str, ttl: int = 3600):
    await redis.expire(f"session:{sid}", ttl)
    expiration_timestamp = time.time() + ttl
    return {"session_id": sid, 
            "expire_time": expiration_timestamp}

async def delete_session(sid: str):
    return await redis.delete(f"session:{sid}")