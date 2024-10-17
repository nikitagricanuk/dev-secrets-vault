from . import connect_db
from psycopg2 import Error
import json

async def create_secret(name: str, secret_data: dict, description: str = None):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    ser_secret_data = json.dumps(secret_data)

    cursor.execute(
        "INSERT INTO secrets (name, description, secret_data) VALUES (%s, %s, %s);",
        (name, description, ser_secret_data,)
    )

    db_connection.commit()
    db_connection.close()

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