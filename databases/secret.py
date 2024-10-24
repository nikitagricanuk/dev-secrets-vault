import databases.user
import fastapi.responses
from . import connect_db
from psycopg2 import Error
import json
import time
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from databases.acl import check_permissions
from databases.acl import check_permissions

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
        select create_secret(%s :: VARCHAR(50), %s :: TEXT, %s :: TEXT[],
            %s :: jsonb, %s :: VARCHAR(50), %s :: TIMESTAMP);
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

#@check_permissions
async def get_secret(secret_id: str = None, secret_name: str = None):
    """
    Returns secret data in json, deserialization needed
    """
    if secret_id is None and secret_name is None:
        return False
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM secrets WHERE secrets.id = %s OR secrets.name = %s;", 
        (secret_id, secret_name,)
    )

    response_secret_data = cursor.fetchone()
    
    secret_id = response_secret_data[0]
    secret_canonical = response_secret_data[1]
    secret_description = response_secret_data[2]
    secret_tags = response_secret_data[3]
    secret_data = response_secret_data[4]
    secret_data_sha256 = response_secret_data[6]
    secret_disabled = response_secret_data[7]

    secret_created_at = response_secret_data[8].isoformat()
    secret_created_at_timestamp = response_secret_data[8].timestamp()

    secret_created_by = response_secret_data[9]

    secret_expires_at = response_secret_data[10].isoformat()
    secret_expires_at_timestamp = response_secret_data[10].timestamp()

    secret_updated_at = response_secret_data[11].isoformat()
    secret_updated_at_timestamp = response_secret_data[11].timestamp()

    return_data = {
        "id": secret_id,
        "canonical": secret_canonical,
        "data": secret_data,
        "sha256": secret_data_sha256,
        "tags": secret_tags,
        "is_disabled": secret_disabled,
        "description": secret_description,
        "created_by": secret_created_by,
        "created_at_timestamp": secret_created_at_timestamp,
        "created_at_utc": secret_created_at,
        "updated_at_timestamp": secret_updated_at_timestamp,
        "updated_at_utc": secret_updated_at,
        "expires_at_timestamp": secret_expires_at_timestamp,
        "expires_at_utc": secret_expires_at,
        "ttl": secret_expires_at_timestamp - secret_created_at_timestamp
    }
    return JSONResponse(content=return_data)

async def get_secret_list():
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM secrets;"
    )

    response_secret_data = cursor.fetchall()

    return_data = []
    for i in range(0, len(response_secret_data)):
        secret_id = response_secret_data[i][0]
        secret_name = response_secret_data[i][1]
        secret_description = response_secret_data[i][2]
        secret_tags = response_secret_data[i][3]
        secret_disabled = response_secret_data[i][7]

        secret_created_at = response_secret_data[i][8].isoformat()
        secret_created_at_timestamp = response_secret_data[i][8].timestamp()

        secret_created_by = response_secret_data[i][9]

        secret_expires_at = response_secret_data[i][10].isoformat()
        secret_expires_at_timestamp = response_secret_data[i][10].timestamp()

        return_data_secret = {
            "id": secret_id,
            "canonical": secret_name,
            "tags": secret_tags,
            "is_disabled": secret_disabled,
            "description": secret_description,
            "created_by": secret_created_by,
            "created_at_timestamp": secret_created_at_timestamp,
            "created_at_utc": secret_created_at,
            "expires_at_timestamp": secret_expires_at_timestamp,
            "expires_at_utc": secret_expires_at,
            "ttl": secret_expires_at_timestamp - secret_created_at_timestamp
        }

        return_data.append(return_data_secret)

    print(return_data)
    return JSONResponse(content=return_data)

# @check_permissions
async def delete_secret(id: str):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        """
        DELETE FROM secrets WHERE id = %s
        RETURNING name;""", 
        (id,)
    )

    db_connection.commit()

    secret_canonical = cursor.fetchone()[0]

    db_connection.close()

    return_data = {
        "id": id,
        "canonical": secret_canonical,
        "deleted_at_timestamp": time.time(),
        "deleted_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat()
    }

    return JSONResponse(content=return_data)

# @check_permissions
async def update_secret(secret_id: str, secret_name: str, secret_data: dict, tags: dict, username: str,  ttl: int = None, description: str = None):
    if secret_id is None and secret_name is None:
        return False
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

    try:
        cursor.execute(
        """
        select update_secret(%s :: UUID,%s :: VARCHAR(50), %s :: TEXT, %s :: TEXT[],
            %s :: jsonb, %s :: VARCHAR(50), %s :: TIMESTAMP);
        """,
        (secret_id, secret_name, description, tags, serialized_secret_data, username, expires_at_timestamp)
        )
    except(Error):
        print("[Error]: ", Error)

    try:
        secret_updated = cursor.fetchone()
    except(Error):
        print("[Error]: ", Error)

    print(secret_updated)

    return_data_secret = {
                        "id": secret_id,
                        "canonical": secret_name,
                        "tags": tags,
                        "is_disabled": False,
                        "description": description,
                        "expires_at_timestamp": expires_at_timestamp,
                        "expires_at_utc": datetime.fromtimestamp(expires_at_timestamp, tz=timezone.utc).isoformat(),
                        "ttl": ttl
                        }

    return JSONResponse(content=return_data_secret)
    

