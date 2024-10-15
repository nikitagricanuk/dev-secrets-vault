from fastapi import FastAPI
from api import router
app = FastAPI() # initializing fastapi

app.include_router(router)

