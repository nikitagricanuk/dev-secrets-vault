from fastapi import FastAPI

app = FastAPI() # initializing fastapi

# Users
@app.post("/v1/users")
async def list_users():
    # тут должна быть бизнес-логика СУБД
    return {"message": "Listing users"}

@app.post("/v1/users/create")
async def create_user():
    return {"message": "Create user"}

# Secrets
@app.post("/v1/secrets/create")
async def create_secret():
    return {"message": "Create secret"}