from fastapi.params import Depends
import uvicorn
from fastapi import FastAPI
from entity.userApp import UserApp
from route.ChatRoute import chat_route
from security.services.authenticateService import get_current_user
from security.route.auth import auth_router



app = FastAPI()
app.include_router(auth_router)
app.include_router(chat_route)
@app.get("/")
def root():
    return {"message": "World World"}
@app.get("/private")
async def hello_user(user:UserApp=Depends(get_current_user)):
    return {"message":"Hello "+user.email}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)