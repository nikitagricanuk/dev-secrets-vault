import psycopg2
from config import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT
from cryptography.passwords import generate_password, generate_password_hash

try:
    conn = psycopg2.connect(database=DB_NAME,
                            host=DB_HOST,
                            user=DB_USERNAME,
                            password=DB_PASSWORD,
                            port=DB_PORT)
except:
    print("Error: Could not connect to the database")
    conn = None

async def create_user(username, email, role, password = None, extra_privileges = {}):
    if conn is None:
        return {"error": "No database connection"}
    
    # Creating a user account
    if password is None:
        password = await generate_password()
    password_hash = await generate_password_hash(password)

    with conn.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash.decode('utf-8')) 
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Setting user role
    await set_user_role(username, role, extra_privileges)

    return {"username": username, 
            "password": password,
            "role": role}

async def set_user_role(username, role, extra_privileges = {}):
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"INSERT INTO roles (username, role_name, extra_privileges) VALUES (\'{username}\', \'{role}\', \'{extra_privileges}\')")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
