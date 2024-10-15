from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Secret(BaseModel):
    data: dict
# Secrets
@router.post("/v1/secrets/create")
async def create_secret(data: Secret):
    return {"message": "Create secret"}
