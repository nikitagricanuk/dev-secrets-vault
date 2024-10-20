from redis import asyncio as aioredis
from config import REDIS_HOST, REDIS_PORT
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from security.settings import get_setting
from utils import str_to_bool
import uuid
import time
import json

redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

async def create_new_session(username: str, session_ip: str):
    ttl = int(await get_setting("auth.session_ttl"))
    sid = str(uuid.uuid4())
    created_at = time.time()

    session_data = {
        "username": username,
        "session_id": sid, # including just in case
        "session_ip": session_ip,
        "created_at": created_at,
        "usage_count": 1
    }

    await redis.setex(f"session:{sid}", ttl, json.dumps(session_data)) # serialize session data and insert into redis database

    return_data =  {"session_id": sid, 
                    "session_ip": session_ip,
                    "username": username,
                    "created_at_timestamp": created_at,
                    "created_at_utc": datetime.fromtimestamp(created_at, tz=timezone.utc).isoformat(),
                    "expires_at_timestamp": time.time() + ttl,
                    "expires_at_utc": (datetime.now(timezone.utc) + timedelta(seconds=ttl)).isoformat(),
                    "remaining_time_seconds": (time.time() + ttl) - created_at,
                    "is_active": True
                    }
        
    return JSONResponse(content=return_data) # serialize and return

async def validate_session(sid: str, host_ip: str):
    """
    Validates a session ID by checking if it exists and if the session's IP matches the host's IP.
    
    Args:
        sid (str): The session ID to validate.
        host_ip (str): The IP address of the host to compare with the session's IP.
        
    Returns:
        int: A status code indicating the result of the validation:
            - 1: Validation successful (session exists, and IP matches).
            - 2: Session does not exist.
            - 3: Session IP does not match the host IP.
            - 4: OTP is set, session token cannot be used more than once
    """
    ip_check = str_to_bool(await get_setting("auth.session_bind_ip"))
    token_otp = str_to_bool(await get_setting("auth.otp_session_token"))

    session_data = await redis.get(f"session:{sid}")
    if session_data:
        session_data = json.loads(session_data) 
        usage_count = session_data["usage_count"]

        if (token_otp is True) and (usage_count >= 1):
            return 4  # Token used more than once (OTP should only be used once)

        usage_count += 1  # Now we increment the usage count since the session exists

        if ip_check:
            session_ip = session_data["session_ip"]
            if host_ip == session_ip:
                return 1  # All good (IP matches)
            else:
                return 3  # IP doesn't match
        else:
            return 1  # All good (no IP check)
    else:
        return 2  # Session doesn't exist

async def renew_session(sid: str, ttl: int = 3600):
    if await redis.expire(f"session:{sid}", ttl):
        session_data = await get_session_data(sid)

        username = session_data["username"]
        created_at = session_data["created_at"]
        session_ip = session_data["session_ip"]
        
        return_data =  {"session_id": sid, 
                        "session_ip": session_ip,
                        "username": username,
                        "created_at_timestamp": created_at,
                        "created_at_utc": datetime.fromtimestamp(created_at, tz=timezone.utc).isoformat(),
                        "expires_at_timestamp": time.time() + ttl,
                        "expires_at_utc": (datetime.now(timezone.utc) + timedelta(seconds=ttl)).isoformat(),
                        "remaining_time_seconds": (time.time() + ttl) - created_at,
                        "is_active": True
                        }
        return JSONResponse(content=return_data)
    

async def delete_session(sid: str):
    old_session_data = await get_session_data(sid)
    await redis.delete(f"session:{sid}")
    session_ip = old_session_data["session_ip"]
    created_at = old_session_data["created_at"]
    username = old_session_data["username"]
    
    return_data =  {"session_id": sid, 
                    "session_ip": session_ip,
                    "username": username,
                    "created_at_timestamp": created_at,
                    "created_at_utc": datetime.fromtimestamp(created_at, tz=timezone.utc).isoformat(),
                    "deleted_at_timestamp": time.time(),
                    "deleted_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat(),
                    "is_active": False
                    }
    return JSONResponse(content=return_data)

async def get_session_data(sid: str):
    session_data = await redis.get(f"session:{sid}")
    if session_data:
        session_data = json.loads(session_data)
        return session_data