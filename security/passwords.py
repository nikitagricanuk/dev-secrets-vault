import string
import random
import bcrypt

async def generate_password(length=12, use_digits=True, use_uppercase=True, use_lowercase=True, use_special_chars=False):
    """
    Generates a random password based on the provided criteria.
    
    :param length: Length of the password (default 12)
    :param use_digits: Include digits in the password (default True)
    :param use_uppercase: Include uppercase letters in the password (default True)
    :param use_lowercase: Include lowercase letters in the password (default True)
    :param use_special_chars: Include special characters in the password (default True)
    :return: Randomly generated password as a string
    """
    characters = ''
    if use_digits:
        characters += string.digits
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character set must be enabled.")

    return ''.join(random.choice(characters) for _ in range(length))

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