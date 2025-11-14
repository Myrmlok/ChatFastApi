from fastapi.params import Depends
import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from entity.userApp import UserApp
from route.ChatRoute import chat_route
from security.services.authenticateService import get_current_user
from security.route.auth import auth_router
from route.UserRoute import user_route
from service.emailService import EmailService
from route.ChatWebsocket import chat_websockets
app = FastAPI()
app.include_router(chat_websockets)
app.include_router(auth_router)
app.include_router(chat_route)
app.include_router(user_route)
@app.get("/")
def root():
    return {"message": "World World"}
@app.get("/private")
async def hello_user(user:UserApp=Depends(get_current_user)):
    return {"message":"Hello "+user.email}
@app.post("/mail")
async def test_mail(to:str):
    if await EmailService.async_send_message(to,"test","hello"):
        return {"message":"ok"}
    return {"message":"false"}
@app.websocket("/ws")
async def testWebSocket(websocket:WebSocket):
    await websocket.accept()
    await websocket.send_text("hello");
    await websocket.close()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)