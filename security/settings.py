import json
from config import PATH_TO_SETTINGS_FILE
from fastapi.responses import JSONResponse


async def get_settings():
    with open(PATH_TO_SETTINGS_FILE, 'r') as fd:
        settings = json.load(fd) 

    return JSONResponse(content=settings)