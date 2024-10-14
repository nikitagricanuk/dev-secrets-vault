from string import ascii_letters, digits
import secrets
import bcrypt

async def generate_password(section_length = 6, number_of_sections = 3):
    alphabet = ascii_letters + digits
    sections = [] # TODO: дописать генерацию паролей
    for i in range(number_of_sections):
        for i in range(section_length):
            sections[0] += i
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

async def compare_password_with_hash(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))