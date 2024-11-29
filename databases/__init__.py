from functools import wraps
import psycopg2
from config import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT

from logging_config import setup_logger

logger = setup_logger(__name__)

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USERNAME, 
                            password=DB_PASSWORD, host=DB_HOST, 
                            port=DB_PORT)
    
def db_connection(func):
    """
    Decorator for establishing database connection.
    This decorator:
        - Provides a cursor object (`cursor`) for executing queries.
        - Automatically closes the connection after the function completes.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Establish a database connection
            db_connection = connect_db()
            cursor = db_connection.cursor()
            kwargs['db_connection'] = db_connection  # Pass connection to the wrapped function
            kwargs['cursor'] = cursor
            return await func(*args, **kwargs)
        except psycopg2.OperationalError as e:
            logger.critical(f"Database connection failed: {e}")
            raise
        except psycopg2.IntegrityError as e:
            logger.error(f"Integrity constraint violated: {e}")
            raise
        except psycopg2.ProgrammingError as e:
            logger.error(f"SQL syntax error or invalid operation: {e}")
            raise
        except psycopg2.DatabaseError as e:
            logger.error(f"Database error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            if db_connection:
                db_connection.close()
    return wrapper