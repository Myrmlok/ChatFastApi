import logging

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.routing import APIRoute
from starlette.websockets import WebSocket

from entity import UserApp, MessageEntity
from security.services.authenticateService import get_current_user
from service.MessageManager import MessageManager

chat_websockets=APIRouter(prefix="/ws/chat",tags=["chat_messages"])
@chat_websockets.websocket("/{chat_id}")
async def connectToChat(websocket:WebSocket,chat_id:int):
    token = websocket.headers.get("Authorization")
    user: UserApp = await get_current_user(token[7:])
    try:
        await websocket.accept()
        await MessageManager.connect(user,websocket,chat_id)
        while(True):
            req= await websocket.receive_json()
            msg=MessageEntity(sender_id=user.id,chat_id=chat_id,text=req['text'])
            await MessageManager.sendMessage(user,msg)
    except Exception as ex:
        logging.error(ex)
        await MessageManager.disconnect(user,chat_id)
        await websocket.close()