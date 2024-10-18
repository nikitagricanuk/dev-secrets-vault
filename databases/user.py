import psycopg2
from psycopg2 import Error
from cryptography.passwords import generate_password, generate_password_hash
from . import connect_db



async def create_user(username, email, role, password = None):
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
        "INSERT INTO users (username, email, password_hash, is_disabled) VALUES (%s, %s, %s, %s);",
        (username, email, password_hash.decode('utf-8'), False,) 
    )

    db_connection.commit()
    db_connection.close()

    # Setting user role
    await set_user_role(username, role)

    return {"username": username, 
            "password": password,
            "role": role}

async def delete_user(username):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "DELETE FROM users WHERE username = %s;", 
        (username,)
    )

    db_connection.commit()
    db_connection.close()

    return {"username": username}

async def set_user_role(username, role):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)


    cursor.execute(
        "INSERT INTO roles (username, role_name) VALUES (%s, %s);",
        (username, role,)
        )
    
    db_connection.commit()
    db_connection.close()


async def get_user(username, uuid = None):
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)
    
    cursor.execute(
        "SELECT * FROM users WHERE username = %s OR id = %s;",
        (username, uuid,)
    )

    data = cursor.fetchone()

    if data == []:
        return False
    
    return data

async def get_users():
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor()
    except(Error):
        print("[Error]: ", Error)

    cursor.execute(
        "SELECT * FROM users;"
    )

    data = cursor.fetchall()

    if data == []:
        return False
    
    return data