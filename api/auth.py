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

@router.post("/v1/auth/token/create")
async def api_create_token():
    return {
        "request_id": "b59c9b74-7a9e-baad-1d15-2d6b7f50b344",
        "lease_id": "",
        "renewable": False,
        "lease_duration": 0,
        "data": None,
        "wrap_info": None,
        "warnings": None,
        "auth": {
            "client_token": "s.NmDre1UnuHKHoDu5mQ1fLnkl",
            "accessor": "mYn5S3xtFIYyQoHwrwX8BExG",
            "policies": ["default"],
            "metadata": {"user": "admin"},
            "lease_duration": 2764800,
            "renewable": True,
            "entity_id": "39a97a27-f0aa-321f-33cb-f6df28a4ae6c",
            "token_type": "service"
        }
    }

@router.post("/v1/auth/token/revoke/{token}")
async def api_revoke_token(token: str):
    return {
        "request_id": "c85f6d6a-6bd4-b0f8-6757-08aa08ec8980",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.post("/v1/auth/token/lookup")
async def api_lookup_token():
    return {
        "request_id": "f3a7f8d3-984b-4fa2-b1c7-7c8d2b44c8d1",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "data": {
            "id": "s.NmDre1UnuHKHoDu5mQ1fLnkl",
            "policies": ["default"],
            "path": "auth/token/create",
            "expire_time": "2024-10-10T10:09:02.87962327Z",
            "entity_id": "39a97a27-f0aa-321f-33cb-f6df28a4ae6c"
        }
    }

@router.post("/v1/auth/token/renew")
async def api_renew_token():
    return {
        "request_id": "a7c9d9e7-df3b-4f56-82d8-34078d354d9c",
        "lease_id": "",
        "renewable": True,
        "lease_duration": 2764800,
        "auth": {
            "client_token": "s.NmDre1UnuHKHoDu5mQ1fLnkl",
            "accessor": "mYn5S3xtFIYyQoHwrwX8BExG",
            "policies": ["default"],
            "metadata": {},
            "lease_duration": 2764800,
            "renewable": True,
            "entity_id": "39a97a27-f0aa-321f-33cb-f6df28a4ae6c",
            "token_type": "service"
        }
    }

# AppRole Authentication
@router.post("/v1/auth/approle/login")
async def api_approle_login():
    return {
        "request_id": "5d7d5b7-3f8e-1f5f-bbcd-6e9e91e2e1a3",
        "lease_id": "",
        "renewable": True,
        "lease_duration": 2764800,
        "auth": {
            "client_token": "s.K2n2f3jl8E1cHgZ8Xz2XJ9wT",
            "accessor": "mYn5S3xtFIYyQoHwrwX8BExG",
            "policies": ["default"],
            "lease_duration": 2764800,
            "renewable": True
        }
    }

# Userpass Authentication
@router.post("/v1/auth/userpass/login/{username}")
async def api_userpass_login(username: str):
    return {
        "request_id": "39a97a27-f0aa-321f-33cb-f6df28a4ae6c",
        "lease_id": "",
        "renewable": True,
        "lease_duration": 2764800,
        "auth": {
            "client_token": "s.XYZ123",
            "accessor": "KYZ123456",
            "policies": ["default"],
            "metadata": {
                "username": username
            },
            "lease_duration": 2764800,
            "renewable": True,
            "entity_id": "98fd50d9-130d-8937-0a95-bf89e72867b7",
            "token_type": "service"
        }
    }

@router.post("/v1/auth/userpass/users/{username}")
async def api_create_user(username: str):
    return {
        "request_id": "b18bbcd5-42b3-f9f8-b5f5-d3a9f08d369d",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.delete("/v1/auth/userpass/users/{username}")
async def api_delete_user(username: str):
    return {
        "request_id": "b3a7f3d7-579d-45d2-95b9-f6207f9f7b29",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }

@router.get("/v1/auth/userpass/users/{username}")
async def api_get_user_info(username: str):
    return {
        "request_id": "d8f6c3a8-92fa-4c7d-9d95-7d8b9145c6f5",
        "data": {
            "policies": ["default", "my-policy"],
            "ttl": 3600,
            "max_ttl": 86400
        }
    }

@router.post("/v1/auth/userpass/users/{username}/password")
async def api_change_password(username: str):
    return {
        "request_id": "cfb6946d-eef6-416e-9201-9b59e5b4a1a6",
        "lease_id": "",
        "lease_duration": 0,
        "renewable": False,
        "warnings": None,
        "auth": None
    }


@router.post("/v1/users")
async def list_users():
    # тут должна быть бизнес-логика СУБД
    return {"message": "Listing users"}

@router.post("/v1/users/create")
async def api_create_user(user: User):
    return await create_user(user.username, user.email, user.role, user.password, user.extra_priveleges)

