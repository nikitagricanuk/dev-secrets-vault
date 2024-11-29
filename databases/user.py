import fastapi.responses
from psycopg2 import DatabaseError, Error, IntegrityError, OperationalError, ProgrammingError
from security.passwords import generate_password, generate_password_hash
from fastapi.responses import JSONResponse
import time
from datetime import datetime, timezone, timedelta
from . import connect_db, db_connection

from logging_config import setup_logger

logger = setup_logger(__name__)

@db_connection
async def create_user(username, email, roles, is_disabled, expires_at=None, password=None, db_connection=None, cursor=None):
    # Creating a user account
    try:
        if password is None:
            password = await generate_password()
            logger.debug("Generated a random password for the user.")

        password_hash = await generate_password_hash(password)
        logger.debug(f"Password hash generated for user {username}.")

        if expires_at is not None:
            expires_at = datetime.fromtimestamp(expires_at).isoformat()
            logger.debug(f"Expire data at set to {expires_at} for user {username}.")

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, roles, is_disabled, expires_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (username, email, password_hash.decode('utf-8'), roles, is_disabled, expires_at)
        )
        db_connection.commit()
        
        logger.info(f"User {username} created successfully.")
        
        uid = cursor.fetchone()[0]

        return_data = {
            "id": uid,
            "created_at_timestamp": time.time(),
            "created_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat(),
            "expires_at_timestamp": expires_at,
            "expires_at_utc": datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat() if expires_at else None,
            "username": username,
            "email": email,
            "roles": roles,
            "disabled": is_disabled,
        }
        return JSONResponse(content=return_data)
    except Exception as e:
        logger.info(f"Failed to create user {username}: {e}")

@db_connection
async def delete_user(username, db_connection=None, cursor=None):
    try:
        cursor.execute(
            """
            DELETE FROM users 
            WHERE username = %s
            RETURNING id;""", 
            (username,)
        )

        db_connection.commit()

        logger.info(f"User {username} deleted successfully.")

        uid = cursor.fetchone()[0]

        return_data =  {"id": uid,
                        "username": username,
                        "deleted_at_timestamp": time.time(),
                        "deleted_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat(),
                        }

        return JSONResponse(content=return_data)
    except Exception as e:
        logger.info(f"Failed to delete user {username}: {e}")

@db_connection
async def get_user(username, uuid = None, db_connection=None, cursor=None):
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s OR id = %s;",
            (username, uuid,)
        )

        data = cursor.fetchone()

        return False if data == [] else data
    except Exception as e:
        logger.info(f"Failed to fetch user details for {username}: {e}")

@db_connection
async def get_users(db_connection=None, cursor=None):
    try:
        cursor.execute(
            "SELECT * FROM users;"
        )

        data = cursor.fetchall()

        return False if data == [] else data
    except Exception as e:
        logger.info(f"Failed to fetch user list: {e}")
