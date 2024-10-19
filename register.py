import asyncio
from databases.user import create_user

async def main():
    username = input("Username: ").strip() or None
    email = input("Email: ").strip() or None
    print("Specify user roles divided by spaces. To make this user admin, add \"admin\" (without brackets) to the roles")
    roles = list(map(str, input("Roles: ").strip().split()))
    is_disabled = bool(input("Is this user disabled (True or False): ").split() or False)
    expires_at = input("Expiration time (timestamp): ").split() or None

    password = input("Password (leave blank to generate automatically): ").strip() or None

    if roles is []:
        exit("You must specify at least one role")
    elif username is None:
        exit("You must specify username")
    elif email is None:
        exit("You must specify email")
    

    await create_user(username, email, roles, is_disabled, expires_at, password)
    
    print("Success")

# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())