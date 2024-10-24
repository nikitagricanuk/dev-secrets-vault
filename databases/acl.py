from . import connect_db
from psycopg2 import Error
from api.session import get_session_data

async def check_permissions(func):
    async def wrapper(session_data: str, action: str, resource_id: str = None, *args, **kwargs):
        
        json = get_session_data(session_data)
        username = json["username"]

        try:
            db_connection = connect_db()
            cursor = db_connection.cursor()
        except(Error):
            print("[Error]: ", Error)

        cursor.execute(
            "select roles from users where username = %s;", 
            (username)
        )

        roles = cursor.fetchone()[0]
        if ('admin' in roles):
            return await func(*args, **kwargs)

        cursor.execute(
            "select permission, username, user_role from acl where resource_id = %s;", 
            (resource_id)
        )

        response_acl = cursor.fetchone()

        if (action in response_acl[0] and response_acl[2] in roles):
            return await func(*args, **kwargs)

        if (action in response_acl[0] and response_acl[1] == username):
            return await func(*args, **kwargs)

        return 1
    return wrapper