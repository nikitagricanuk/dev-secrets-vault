from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()
# Database settings
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

app = FastAPI() # initializing fastapi

# Users
@app.post("/v1/users")
async def list_users():
    # тут должна быть бизнес-логика СУБД
    return {"message": "Listing users"}

@app.post("/v1/users/create")
async def create_user():
    return {"message": "Create user"}

# Secrets
@app.post("/v1/secrets/create")
async def create_secret():
    return {"message": "Create secret"}