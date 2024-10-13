from fastapi import FastAPI
from api.api import router
app = FastAPI() # initializing fastapi

app.include_router(router)

