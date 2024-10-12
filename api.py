from pydantic import BaseModel
from databases.db import create_user
from fastapi import APIRouter

router = APIRouter()

# Users

class User(BaseModel):
    username: str
    email: str
    role: str
    password: str
    extra_priveleges: dict = None

@router.post("/v1/users")
async def list_users():
    # тут должна быть бизнес-логика СУБД
    return {"message": "Listing users"}

@router.post("/v1/users/create")
async def api_create_user(user: User):
    return await create_user(user.username, user.email, user.role, user.password, user.extra_priveleges)


# Secrets
@router.post("/v1/secrets/create")
async def create_secret():
    return {"message": "Create secret"}