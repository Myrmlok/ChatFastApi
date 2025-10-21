from fastapi.params import Depends
import uvicorn
from fastapi import FastAPI
from config.db import create_all_tables
from entity.userApp import UserApp
from security.services.authenticateService import get_current_user
from security.route.auth import auth_router

create_all_tables()

app = FastAPI()
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "World World"}
@app.get("/private")
async def hello_user(user:UserApp=Depends(get_current_user)):
    return {"message":"Hello "+user.username}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)