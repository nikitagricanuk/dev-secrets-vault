from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api import router
from config import CORS_ORIGINS_LIST
from security.settings import get_setting
from utils import str_to_bool

from logging_config import setup_logger

logger = setup_logger(__name__)

app = FastAPI() # initializing fastapi

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS_LIST,
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

# HTTPs-only check
@app.middleware("http")
async def enforce_https(request: Request, call_next):
    try:
        https_only_value = await get_setting("security.https_only")
        https_only = str_to_bool(https_only_value)

        # Check if HTTPS is required and connection is not over HTTPS
        if https_only and request.url.scheme != "https":
            return JSONResponse(status_code=400, content={"detail": "HTTPS required"})

        # Proceed with the normal request flow
        return await call_next(request)
    except Exception as e:
        logger.error(f"HTTPs enforcing error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract error details
    errors = exc.errors()
    error_details = [
        {
            "loc": error["loc"],  # Location of the error (e.g., body, query, path)
            "msg": error["msg"],  # Error message
            "type": error["type"],  # Type of the error (e.g., value_error, type_error)
        }
        for error in errors
    ]
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": error_details,
        },
    )

app.include_router(router)

