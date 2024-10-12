import psycopg2
from main import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT

conn = psycopg2.connect(database=DB_NAME,
                        host=DB_HOST,
                        user=DB_USERNAME,
                        password=DB_PASSWORD,
                        port=DB_PORT)

