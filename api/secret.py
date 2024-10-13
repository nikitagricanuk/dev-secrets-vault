from fastapi import APIRouter

router = APIRouter()

# Secrets
@router.post("/v1/secrets/create")
async def create_secret():
    return {"message": "Create secret"}
