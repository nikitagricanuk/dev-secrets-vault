from fastapi import APIRouter, Depends
from pydantic import BaseModel
from security.settings import get_settings_list, get_setting, set_setting
from api.auth import authenticate_user_token

router = APIRouter()

class Setting(BaseModel):
    key: str
    value: str

@router.get("/v1/sys/settings")
async def api_set_settings_list(session_data: str = Depends(authenticate_user_token)):
    return await get_settings_list()

@router.get("/v1/sys/settings/{setting_key}")
async def api_get_setting(setting_key: str, session_data: str = Depends(authenticate_user_token)):
    return await get_setting(setting_key)

@router.post("/v1/sys/settings")
async def api_set_setting(setting: Setting, session_data: str = Depends(authenticate_user_token)):
    return await set_setting(setting.key, setting.value)
