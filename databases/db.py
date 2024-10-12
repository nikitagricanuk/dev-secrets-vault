import psycopg2
from main import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT
from cryptography.passwords import generate_password_hash

try:
    conn = psycopg2.connect(database=DB_NAME,
                            host=DB_HOST,
                            user=DB_USERNAME,
                            password=DB_PASSWORD,
                            port=DB_PORT)
except:
    print("Error: Could not connect to the database")

async def create_user(username, email, role, password = None, extra_privileges = None):
    # Creating a user account
    password_hash = generate_password_hash(password)

    with conn.cursor() as cursor:
        try:
            cursor.execute(f"INSERT INTO users (username, email, password_hash) VALUES ({username}, {email}, {password_hash})")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Setting user role
    set_user_role(username, role, extra_privileges)

async def set_user_role(username, role, extra_privileges = None):
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"INSERT INTO roles (username, role, extra_privileges) VALUES ({username}, {role}, {extra_privileges})")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
