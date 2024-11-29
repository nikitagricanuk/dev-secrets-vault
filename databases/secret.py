import databases.user
import fastapi.responses
from . import connect_db, db_connection
from psycopg2 import Error
import json
import time
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse
from databases.acl import check_permissions
from databases.acl import check_permissions

from logging_config import setup_logger

logger = setup_logger(__name__)

@db_connection
async def create_secret(name: str, secret_data: dict, tags: dict, username: str,  ttl: int = None, description: str = None, db_connection=None, cursor=None):
    try:
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
        
        logger.info(f"Secret {name} created successfully.")

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
    except Exception as e:
        logger.info(f"Failed to create secret {name}: {e}")

@db_connection
async def get_secret(secret_id: str = None, secret_name: str = None, db_connection=None, cursor=None):
    """
    Returns secret data in json, decryption handled
    """
    try:
        if secret_id is None and secret_name is None:
            return False

        cursor.execute(
            """
            SELECT secrets.id, secrets.name, secrets.description, secrets.tags,
                pgp_sym_decrypt(secrets.secret_data::bytea, (SELECT crypto_key FROM userkeys WHERE username = secrets.created_by)) AS secret_data,
                secrets.secret_data_hashsum, secrets.is_disabled, secrets.created_at,
                secrets.created_by, secrets.expires_at, secrets.updated_at
            FROM secrets 
            WHERE secrets.id = %s OR secrets.name = %s;
            """,
            (secret_id, secret_name,)
        )

        response_secret_data = cursor.fetchone()

        if not response_secret_data:
            logger.info(f"Secret with ID {secret_id} not found")
            return JSONResponse(status_code=404, content={"detail": "Secret not found"})
        
        secret_created_at_timestamp = response_secret_data[7].timestamp()

        if secret_expires_at := response_secret_data[9]:
            secret_expires_at_iso = secret_expires_at.isoformat()
            secret_expires_at_timestamp = secret_expires_at.timestamp()
        else:
            secret_expires_at_iso = None
            secret_expires_at_timestamp = None

        return_data = {
            "id": response_secret_data[0],
            "canonical": response_secret_data[1],
            "data": response_secret_data[4],  # Decrypted data
            "sha256": response_secret_data[5],
            "tags": response_secret_data[3],
            "is_disabled": response_secret_data[6],
            "description": response_secret_data[2],
            "created_by": response_secret_data[8],
            "created_at_timestamp": response_secret_data[7].timestamp(),
            "created_at_utc": response_secret_data[7].isoformat(),
            "updated_at_timestamp": response_secret_data[10].timestamp(),
            "updated_at_utc": response_secret_data[10].isoformat(),
            "expires_at_timestamp": secret_expires_at_timestamp,
            "expires_at_utc": secret_expires_at_iso,
            "ttl": secret_expires_at_timestamp - secret_created_at_timestamp if secret_expires_at_timestamp else None
        }
        return JSONResponse(content=return_data)

    except Exception as e:
        logger.info(f"Failed to fetch secret details for secret with ID {secret_id} (Name: {secret_name}): {e}")

@db_connection
async def get_secret_list(db_connection=None, cursor=None):
    try:
        cursor.execute(
            "SELECT * FROM secrets;"
        )

        response_secret_data = cursor.fetchall()
        # [('0a795ef8-4d4e-412c-874c-bbac610779f5', 'my_secret', 'This is a secret for API key', 
        # ['backend', 'devops'], <memory at 0xffff89fa1f00>, '6b3a5e71ce76bcbcf0aba823965c8e62', 
        # False, datetime.datetime(2024, 10, 25, 10, 15, 35, 405241), 'nikitagricanuk', 
        # datetime.datetime(2024, 10, 25, 11, 15, 35, 405129), 
        # datetime.datetime(2024, 10, 25, 10, 15, 35, 405241))]
        
        return_data = []
        for i in range(len(response_secret_data)): # TODO: refactor this section
            secret_id = response_secret_data[i][0]
            secret_name = response_secret_data[i][1]
            secret_description = response_secret_data[i][2]
            secret_tags = response_secret_data[i][3]
            secret_disabled = response_secret_data[i][6]

            secret_created_at = response_secret_data[i][7].isoformat()
            secret_created_at_timestamp = response_secret_data[i][7].timestamp()

            secret_created_by = response_secret_data[i][8]

            secret_expires_at = response_secret_data[i][9].isoformat()
            secret_expires_at_timestamp = response_secret_data[i][9].timestamp()

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

        return JSONResponse(content=return_data)
    except Exception as e:
        logger.info(f"Failed to fetch secrets: {e}")

@db_connection
async def delete_secret(id: str, db_connection=None, cursor=None):
    try:
        cursor.execute(
            """
            DELETE FROM secrets WHERE id = %s
            RETURNING name;""", 
            (id,)
        )

        db_connection.commit()

        secret_canonical = cursor.fetchone()[0]

        return_data = {
            "id": id,
            "canonical": secret_canonical,
            "deleted_at_timestamp": time.time(),
            "deleted_at_utc": datetime.fromtimestamp(time.time(), tz=timezone.utc).isoformat()
        }

        return JSONResponse(content=return_data)
    except Exception as e:
        logger.info(f"Failed to delete secret with ID {id}: {e}")

@db_connection
async def update_secret(secret_id: str, secret_name: str, secret_data: dict, tags: dict, username: str,  ttl: int = None, description: str = None, db_connection=None, cursor=None):
    try:
        if secret_id is None and secret_name is None:
            return False

        expires_at_timestamp = None
        # Calculate expires_at_timestamp based on ttl
        if ttl is not None:
            # Convert ttl (seconds) to a future timestamp
            expires_at_timestamp = datetime.fromtimestamp(time.time() + ttl).isoformat()

        serialized_secret_data = json.dumps(secret_data)

        cursor.execute(
        """
        select update_secret(%s :: UUID,%s :: VARCHAR(50), %s :: TEXT, %s :: TEXT[],
            %s :: jsonb, %s :: VARCHAR(50), %s :: TIMESTAMP);
        """,
        (secret_id, secret_name, description, tags, serialized_secret_data, username, expires_at_timestamp)
        )
        
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
    except Exception as e:
        logger.info(f"Error updating secret with ID '{secret_id}': {e}")

