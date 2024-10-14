import psycopg2
from psycopg2 import Error
from config import DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT
from cryptography.passwords import generate_password, generate_password_hash

def connect_db():
    return psycopg2.connect(database=DB_NAME, user=DB_USERNAME, 
                            password=DB_PASSWORD, host=DB_HOST, 
                            port=DB_PORT)


async def create_user(username, email, role, password = None, extra_privileges = {}):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)
    
    # Creating a user account
    if password is None:
        password = await generate_password()
    password_hash = await generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (username, email, password_hash, is_disabled) VALUES (%s, %s, %s, %s)",
        (username, email, password_hash.decode('utf-8'), False,) 
    )

    db_connection.commit()
    db_connection.close()

    # Setting user role
    await set_user_role(username, role, extra_privileges)

    return {"username": username, 
            "password": password,
            "role": role}

async def set_user_role(username, role, extra_privileges = {}):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)


    cursor.execute(
        "INSERT INTO roles (username, role_name, extra_privileges) VALUES (%s, %s, %s)",
        (username, role, extra_privileges,)
        )
    
    db_connection.commit()
    db_connection.close()


async def get_user(username):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)
    
    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )

    data = cursor.fetchone()

    if data == []:
        return False
    
    return data