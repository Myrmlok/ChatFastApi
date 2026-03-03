import base64
import json
import os
from datetime import datetime

import cv2
import numpy as np
from fastapi.params import Depends
import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket

from entity.userApp import UserApp
from route.HallRoute import hall_route

from security.services.authenticateService import get_current_user
from security.route.auth import auth_router
from route.UserRoute import user_route
from service.emailService import EmailService
app = FastAPI()

app.include_router(auth_router)
app.include_router(user_route)
app.include_router(hall_route)
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
WEBSOCKET_FRAMES_DIR = "websocket_frames"
os.makedirs(WEBSOCKET_FRAMES_DIR, exist_ok=True)
@app.websocket("/ws")
async def testWebSocket(websocket:WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.receive_text()
        data = json.loads(message)
        img_data = data['image']
        if ',' in img_data:
            img_data = img_data.split(',')[1]
        timestamp = data.get('timestamp', datetime.now().isoformat())
        img_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        filename = f"{WEBSOCKET_FRAMES_DIR}/frame_{timestamp}.jpg"

        cv2.imwrite(filename, frame)
    await websocket.close()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)