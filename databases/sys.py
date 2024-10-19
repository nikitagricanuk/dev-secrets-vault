from . import connect_db
from psycopg2 import Error
import json

async def create_setting(scope_type: str, scope: str, setting_key: str,
                             setting_value: str):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        """
        INSERT INTO settings (scope_type, scope, setting_key, setting_value) 
        VALUES (%s, %s, %s, %s);
        """, (scope_type, scope, setting_key, setting_value,)
    )

    db_connection.commit()
    db_connection.close()

async def get_all_settings():
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM security_settings;"
    )

    data = cursor.fetchall()

    return data

    

async def get_setting(setting_key: str):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM security_settings WHERE setting_key = %s;",
        (setting_key,)
    )

    data = cursor.fetchone()

    return data

    