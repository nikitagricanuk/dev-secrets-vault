from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .auth import authenticate_user_token
from databases.secret import create_secret, get_secret, get_secret_list, delete_secret, update_secret
from typing import List

router = APIRouter()

class Secret(BaseModel):
    name: str
    data: dict
    tags: List[str]
    ttl: int = None
    description: str = None

# Secrets
@router.post("/v1/secrets/create")
async def api_create_secret(secret_data: Secret, 
                            session_data: str = Depends(authenticate_user_token)):
    return await create_secret(secret_data.name, secret_data.data, 
                        secret_data.tags, session_data["username"],
                        secret_data.ttl, secret_data.description)

@router.get("/v1/secrets/{secret_id}")
async def api_get_secret(secret_id: str, session_data: str = Depends(authenticate_user_token)):
<<<<<<< HEAD
    # return await get_secret(secret_id, session_data=session_data, action='read', resource_id=secret_id)
    return await get_secret(secret_id)
=======
    return await get_secret(secret_id, session_data=session_data, action='read', resource_id=secret_id)
>>>>>>> dev

@router.get("/v1/secrets")
async def api_get_all_secrets(session_data: str = Depends(authenticate_user_token)):
    return await get_secret_list()

@router.delete("/v1/secrets/{secret_id}")
async def api_delete_secret(secret_id: str, session_data: str = Depends(authenticate_user_token)):
<<<<<<< HEAD
    # return await delete_secret(secret_id, session_data=session_data, action='delete', resource_id=secret_id)
    return await delete_secret(secret_id)
=======
    return await delete_secret(secret_id, session_data=session_data, action='delete', resource_id=secret_id)
>>>>>>> dev

@router.post("/v1/secrets/update/{secret_id}")
async def api_secret_update(secret_id: str, secret_data: Secret, session_data: str = Depends(authenticate_user_token)):
    return await update_secret(secret_id, secret_data.name, secret_data.data, 
                        secret_data.tags, session_data["username"],
                        secret_data.ttl, secret_data.description,
                        session_data=session_data, action='update', resource_id=secret_id)