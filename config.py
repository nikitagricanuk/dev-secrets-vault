# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

PATH_TO_SETTINGS_FILE = os.getenv('PATH_TO_SETTINGS_FILE')

CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost,http://127.0.0.1')
CORS_ORIGINS_LIST = [origin.strip() for origin in CORS_ORIGINS.split(',') if origin.strip()]

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()