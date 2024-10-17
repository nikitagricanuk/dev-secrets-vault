import databases.user
import fastapi.responses
from . import connect_db
from psycopg2 import Error
import json
import time
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse

async def create_secret(name: str, secret_data: dict, tags: dict, username: str,  ttl: int = None, description: str = None):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    expires_at_timestamp = None
    # Calculate expires_at_timestamp based on ttl
    if ttl is not None:
        # Convert ttl (seconds) to a future timestamp
        expires_at_timestamp = datetime.fromtimestamp(time.time() + ttl).isoformat()



    serialized_secret_data = json.dumps(secret_data)

    cursor.execute(
        """
        INSERT INTO secrets (name, description, tags, secret_data, created_by, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (name, description, tags, serialized_secret_data, username, expires_at_timestamp,)
    )

    db_connection.commit()

    secret_id = cursor.fetchone()[0]

    db_connection.close()

    return_data = {
        "secret_id": secret_id,
        "created_at_timestamp": time.time(),
        "created_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat(),
        "expires_at_timestamp": (time.time() + ttl) if ttl is not None else None,
        "expires_at_utc": (datetime.now(timezone.utc) + timedelta(seconds=ttl)).isoformat() if ttl is not None else None,
        "ttl": ttl,
        "tags": tags,
        "is_active": True,
        "created_by": username,
        "description": description
    }
    return JSONResponse(content=return_data)

async def get_secret(secret_id: str, secret_name: str):
    """
    Returns secret data in json, deserialization needed
    """
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM secrets WHERE id = %s OR name = %s", 
        (secret_id, secret_name,)
    )

    secret_data = cursor.fetchone()

    return secret_data