from fastapi import APIRouter
from pydantic import BaseModel
from databases.db import create_user

router = APIRouter()

class User(BaseModel):
    username: str
    email: str
    role: str
    password: str = None
    extra_priveleges: dict = {}

@router.post("/v1/users")
async def list_users():
    # тут должна быть бизнес-логика СУБД
    return {"message": "Listing users"}

@router.post("/v1/users/create")
async def api_create_user(user: User):
    return await create_user(user.username, user.email, user.role, user.password, user.extra_priveleges)

