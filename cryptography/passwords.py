from string import ascii_letters, digits
import secrets
import bcrypt

async def generate_password(section_length = 6, number_of_sections = 3):
    alphabet = ascii_letters + digits
    sections = ''.join(secrets.choice(alphabet) for _ in range(section_length) for _ in range(number_of_sections))
    password = '-'.join(sections)
    return password

async def generate_password_hash(password = None):
    if password is None:
        password = await generate_password()

    salt = bcrypt.gensalt() # generate salt to improve password security

    hashed_password =  bcrypt.hashpw(password.encode('utf8'), salt)

    if not(bcrypt.checkpw(password.encode('utf-8'), hashed_password)):
        await generate_password_hash(password)

    return hashed_password

