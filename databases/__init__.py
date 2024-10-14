import psycopg2
from config import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USERNAME, 
                            password=DB_PASSWORD, host=DB_HOST, 
                            port=DB_PORT)