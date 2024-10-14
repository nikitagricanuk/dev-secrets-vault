from fastapi import APIRouter

router = APIRouter()

@router.post("/v1/sys/auth")
async def api_auth_methods():
    return {"message": "test"}