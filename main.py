from fastapi import FastAPI, Request, HTTPException
from api import router
from security.settings import get_setting
from utils import str_to_bool
from fastapi.responses import JSONResponse
app = FastAPI() # initializing fastapi

@app.middleware("http")
async def enforce_https(request: Request, call_next):
    try:
        https_only_value = await get_setting("security.https_only")
        https_only = str_to_bool(https_only_value)

        # Check if HTTPS is required and connection is not over HTTPS
        if https_only and request.url.scheme != "https":
            return JSONResponse(status_code=400, content={"detail": "HTTPS required"})

        # Proceed with the normal request flow
        response = await call_next(request)
        return response

    except Exception as e:
        # logging.error(f"Error in enforce_https middleware: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(router)

