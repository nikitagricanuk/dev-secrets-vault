from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from databases.db import create_user, get_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from cryptography.passwords import compare_password_with_hash
from api.session import create_new_session, validate_session, delete_session, renew_session
from config import JWT_SECRET_KEY

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token/create")

async def authenticate_user_password(username: str, password: str):
    data = await get_user(username)
    if data is False: 
        return False # User doesn't exist
    
    if await compare_password_with_hash(password, data[3]):
        return True

    return False

security = HTTPBearer()
async def authenticate_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    username = await validate_session(credentials.credentials)
    if username: 
        return username
    raise HTTPException(status_code=401, detail="Invalid token or session expired")

class User(BaseModel):
    username: str
    email: str
    role: str
    password: str = None
    extra_priveleges: dict = {}

@router.post("/v1/auth/token/create")
async def api_create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if await authenticate_user_password(form_data.username, form_data.password):
        return await create_new_session(form_data.username)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/v1/auth/token/renew")
async def api_renew_token(username: str = Depends(authenticate_user_token)):
    return {'username': username}
    
@router.post("/v1/auth/token/revoke")
async def api_revoke_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if await validate_session(credentials.credentials):
        await delete_session(credentials.credentials)
        return {"message": "Session revoked successfully"}

    raise HTTPException(status_code=401, detail="Invalid token or session expired")


# @router.post("/v1/auth/users")
# async def list_users():
#     # тут должна быть бизнес-логика СУБД
#     return {"message": "Listing users"}

@router.post("/v1/auth/users/create")
async def api_create_user(user: User):
    return await create_user(user.username, user.email, user.role, user.password, user.extra_priveleges)

# @router.delete("/v1/auth/users/{user.username}") # TODO: rewrite this correctly
# async def api_delete_user(user: User):
#     return {"message": "test"} 

