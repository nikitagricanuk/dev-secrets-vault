import fastapi.responses
from psycopg2 import Error
from cryptography.passwords import generate_password, generate_password_hash
from fastapi.responses import JSONResponse
import time
from datetime import datetime, timezone, timedelta
from . import connect_db

async def create_user(username, email, roles, is_disabled, expires_at = None, password = None):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)
    
    # Creating a user account
    if password is None:
        password = await generate_password()
    password_hash = await generate_password_hash(password)
    
    if expires_at is not None:
        expires_at = datetime.fromtimestamp(expires_at).isoformat()

    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, roles, is_disabled, expires_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (username, email, password_hash.decode('utf-8'), roles, is_disabled, expires_at,)
    )

    db_connection.commit()

    uid = cursor.fetchone()[0]
    db_connection.close()

    return_data =  {"id": uid,
                    "created_at_timestamp": time.time(),
                    "created_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat(),
                    "expires_at_timestamp": expires_at,
                    "expires_at_utc": datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat() if expires_at is not None else None,
                    "username": username,
                    "email": email,
                    "roles": roles,
                    "disabled": is_disabled
                    }
    
    return JSONResponse(content=return_data)

async def delete_user(username):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "DELETE FROM users WHERE username = %s;", 
        (username,)
    )

    db_connection.commit()
    db_connection.close()

    return {"username": username}

async def get_user(username, uuid = None):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)
    
    cursor.execute(
        "SELECT * FROM users WHERE username = %s OR id = %s;",
        (username, uuid,)
    )

    data = cursor.fetchone()

    if data == []:
        return False
    
    return data

async def get_users():
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM users;"
    )

    data = cursor.fetchall()

    if data == []:
        return False
    
    return data