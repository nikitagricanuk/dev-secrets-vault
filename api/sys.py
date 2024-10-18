from fastapi import APIRouter

router = APIRouter()

@router.post("/v1/sys/security")
async def api_auth_methods():
    return {"message": "test"}

@router.post("/v1/sys/acl")
async def api_auth_methods():
    return {"message": "test"}