from . import connect_db, db_connection
from psycopg2 import Error
import json

from logging_config import setup_logger

logger = setup_logger(__name__)

@db_connection
async def create_setting(scope_type: str, scope: str, setting_key: str,
                            setting_value: str, db_connection=None, cursor=None):
    try:
        cursor.execute(
            """
            INSERT INTO settings (scope_type, scope, setting_key, setting_value) 
            VALUES (%s, %s, %s, %s);
            """, (scope_type, scope, setting_key, setting_value,)
        )

        db_connection.commit()
        
        logger.info(f"Set setting {setting_key} to {setting_value}")
    except Exception as e:
        logger.info(f"Failed to set setting {setting_key} to {setting_value}: {e}")

@db_connection
async def get_all_settings(db_connection=None, cursor=None):
    try:
        cursor.execute(
            "SELECT * FROM security_settings;"
        )

        return cursor.fetchall()
    except Exception as e:
        logger.info(f"Failed to fetch settings: {e}")
    
@db_connection
async def get_setting(setting_key: str, db_connection=None, cursor=None):
    try:
        cursor.execute(
            "SELECT * FROM security_settings WHERE setting_key = %s;",
            (setting_key,)
        )

        return cursor.fetchone()
    except Exception as e:
        logger.info(f"Failed to fetch setting {setting_key}: {e}")
