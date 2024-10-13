from fastapi import APIRouter
from api.auth import router as auth_router
from api.secret import router as secret_router
from api.sys import router as sys_router
from api.transit import router as transit_router

router = APIRouter() # Main router

# Including routers
router.include_router(auth_router)
router.include_router(secret_router)
router.include_router(sys_router)
router.include_router(transit_router)