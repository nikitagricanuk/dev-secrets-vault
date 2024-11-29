from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from databases.user import create_user, get_user, get_users, delete_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from security.passwords import compare_password_with_hash
from api.session import create_new_session, validate_session, delete_session, renew_session, get_session_data
from logging_config import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token/create")

async def authenticate_user_password(username: str, password: str):
    data = await get_user(username)
    if data is False:
        logger.info(f"Failed to authenticate user {username}: the user does not exist")
        return False # User doesn't exist

    return bool(await compare_password_with_hash(password, data[3]))

security = HTTPBearer()
async def authenticate_user_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    status = await validate_session(credentials.credentials, request.client.host)
    if status == 1:
        return await get_session_data(credentials.credentials)
    elif status == 2:
        logger.info(f"Failed to authenticate token {credentials.credentials}: Invalid token or session expired")
        raise HTTPException(status_code=401, detail="Invalid token or session expired")
    elif status == 3:
        logger.info(f"Failed to authenticate token {credentials.credentials}: Session IP doesn't match with host IP")
        raise HTTPException(status_code=401, detail="Session IP doesn't match with host IP")

class User(BaseModel):
    username: str
    email: str
    roles: list
    password: str = None

@router.post("/v1/auth/token/create")
async def api_create_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    logger.debug(f"Attempting to authenticate user {form_data.username}...")
    if await authenticate_user_password(form_data.username, form_data.password):
        logger.info(f"User {form_data.username} authenticated successfully.")
        return await create_new_session(form_data.username, request.client.host)
    
    logger.info(f"Failed to authenticate user {form_data.username}: Incorrect username or password.")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/v1/auth/token/renew")
async def api_renew_token(session_data: str = Depends(authenticate_user_token)):
    logger.info(f"Token renewal initiated by user {session_data['username']}.")
    return await renew_session(session_data["session_id"])
        
@router.post("/v1/auth/token/revoke")
async def api_revoke_token(session_data: str = Depends(authenticate_user_token)):
    logger.info(f"Token revocation initiated by user {session_data['username']}.")
    return await delete_session(session_data["session_id"])

@router.post("/v1/auth/users/create")
async def api_create_user(user: User, session_data: str = Depends(authenticate_user_token)):
    logger.info(f"User creation initiated by user '{session_data['username']}' for new user '{user.username}'.")
    return await create_user(user.username, user.email, user.roles, False, None, user.password)

@router.delete("/v1/auth/users/{username}")
async def api_delete_user(username: str, session_data: str = Depends(authenticate_user_token)):
    logger.info(f"User deletion initiated by user {username} for user {username}.")
    return await delete_user(username)
