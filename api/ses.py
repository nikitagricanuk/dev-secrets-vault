from redis import asyncio as aioredis
from config import REDIS_HOST, REDIS_PORT
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
import uuid
import time
import json

redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

async def create_new_session(username: str, session_ip: str, ttl: int = 3600):
    """
    Creates a new session for a user and stores the session data.

    Arguments:
    username (str): The username for the new session.
    session_ip (str): The IP address of the user initiating the session.
    ttl (int, optional): The time-to-live for the session in seconds (default is 3600 seconds).

    Returns:
    dict: A dictionary containing the session details, including:
        - session_id (str): A unique identifier for the session.
        - username (str): The username associated with the session.
        - session_ip (str): The IP address of the user.
        - created_at (float): The timestamp of when the session was created.
    """

    sid = str(uuid.uuid4())
    created_at = time.time()

    session_data = {
        "username": username,
        "session_id": sid, # including just in case
        "session_ip": session_ip,
        "created_at": created_at
    }

    await redis.setex(f"session:{sid}", ttl, json.dumps(session_data)) # serialize session data and insert into redis database

    """
    Creates a new session and stores it in the Redis database.

    Arguments:
    sid (str): A unique session identifier.
    ttl (int): The session's time-to-live in seconds.
    session_data (dict): The session data to be serialized and stored.
    session_ip (str): The IP address of the user initiating the session.
    username (str): The username associated with the session.

    Returns:
    dict: A dictionary containing session information, including:
        - session_id (str): The session identifier.
        - session_ip (str): The user's IP address.
        - username (str): The username.
        - created_at_timestamp (float): The timestamp of when the session was created.
        - created_at_utc (str): The creation time of the session in UTC format.
        - expires_at_timestamp (float): The timestamp of when the session will expire.
        - expires_at_utc (str): The expiration time of the session in UTC format.
        - remaining_time_seconds (float): The remaining time of the session in seconds.
        - is_active (bool): The status of the session's activity (True if active).
    """

    # Prepare the return dictionary with session data
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
    """
    ip_check = True  # TODO: replace with the value from the db
    session_data = await redis.get(f"session:{sid}")
    
    """
    Validates the session associated with a given session ID and checks the IP address if required.

    Arguments:
    sid (str): The unique session identifier.
    host_ip (str): The IP address of the user attempting to access the session.

    Returns:
    int: An integer representing the validation result:
        - 1: Session is valid and IP address matches (or no IP check).
        - 2: Session does not exist.
        - 3: Session IP does not match the host IP.
    """

    if session_data:
        if ip_check:
            session_data = json.loads(session_data)
            session_ip = session_data["session_ip"]

            if host_ip == session_ip:
                return 1  # All good
            else:
                return 3  # Session IP doesn't match with host IP
        else:
            return 1  # All good (no IP check)
    else:
        return 2  # Session doesn't exist

async def renew_session(sid: str, ttl: int = 3600):
    
    """
    Renews the session identified by the given session ID (sid) by extending its expiration time.

    This function checks if the session is still valid and, if so, retrieves its associated data,
    including the username and IP address. It then constructs a response with session details
    and updates the expiration timestamp.

    Parameters:
    - sid (str): The session ID of the session to be renewed.
    - ttl (int, optional): The time-to-live (TTL) for the session in seconds. 
    Defaults to 3600 seconds (1 hour).

    Returns:
    - JSONResponse: A JSON response containing the renewed session details including:
        - session_id (str): The ID of the session.
        - session_ip (str): The IP address associated with the session.
        - username (str): The username of the user associated with the session.
        - created_at_timestamp (int): The timestamp when the session was created.
        - created_at_utc (str): The creation time of the session in UTC format.
        - expires_at_timestamp (int): The timestamp when the session will expire.
        - expires_at_utc (str): The expiration time of the session in UTC format.
        - remaining_time_seconds (int): The remaining time until the session expires in seconds.
        - is_active (bool): A flag indicating that the session is active.

    Raises:
    - Exception: Raises an exception if there is an error retrieving session data 
    or if the session ID is invalid.
    """

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

    """
    Deletes a session from the Redis database and returns details about the deleted session.

    Arguments:
    sid (str): The unique session identifier of the session to be deleted.

    Returns:
    JSONResponse: A response containing details of the deleted session, including:
        - session_id (str): The identifier of the deleted session.
        - session_ip (str): The IP address associated with the session.
        - username (str): The username associated with the session.
        - created_at_timestamp (float): The timestamp of when the session was created.
        - created_at_utc (str): The creation time of the session in UTC format.
        - deleted_at_timestamp (float): The timestamp of when the session was deleted.
        - deleted_at_utc (str): The deletion time of the session in UTC format.
        - is_active (bool): The status indicating that the session has been deleted (False).
    """

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

    """
    Retrieves session data from the Redis database using the session ID.

    Arguments:
    sid (str): The unique session identifier for which to retrieve data.

    Returns:
    dict: A dictionary containing the session data if the session exists; otherwise, None.
    """

    session_data = await redis.get(f"session:{sid}")
    if session_data:
        session_data = json.loads(session_data)
        return session_data	