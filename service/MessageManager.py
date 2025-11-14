import logging
from datetime import datetime
from typing import Dict, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from config.db import connection
from entity import UserApp, MessageEntity
from exceptions.UsersExceptions import UserNotFoundException
from repository.MessageRepository import MessageRepository
from repository.chatRepository import ChatRepository
from service.chatService import ChatService
from service.userService import UserService


class MessageManager:
    connections: Dict[int,Dict[UUID,WebSocket]]={}
    @classmethod
    @connection
    async def connect(cls,user:UserApp,websocket:WebSocket,chat_id:int,session):
        find_chat=await ChatRepository.get_chat_with_users(session,chat_id)
        if not any(user.id==el.id for el in find_chat.users):
            raise UserNotFoundException()
        if find_chat.id not in cls.connections:
            cls.connections[find_chat.id]= {}
        else:
            await cls.broadcast_to_room(user.id,find_chat.id,{"message":"user online","user":str(user.id)})
        cls.connections[find_chat.id][user.id]=websocket
    @classmethod
    async def disconnect(cls,user:UserApp,chat_id:int):
        if chat_id in cls.connections:
            cls.connections[chat_id].pop(user.id)
            if not cls.connections[chat_id]:
                del cls.connections[chat_id]
            else:
                await cls.broadcast_to_room(user.id,chat_id,{"message":"userDisconnect","user":str(user.id)})

    @classmethod
    @connection
    async def sendMessage(cls,sender:UserApp,message:MessageEntity,session):
        if not any(sender.id==el for el in cls.connections[message.chat_id].keys()):
            raise UserNotFoundException()
        await MessageRepository.add(session, message)
        await cls.broadcast_to_room(sender.id,message.chat_id,{"sender_id":str(message.sender_id),"text":message.text})
    @classmethod
    async def broadcast_to_room(cls,sender_id:UUID,room_id:int,data:dict):
        if room_id in cls.connections:
            user_to_websocket=cls.connections[room_id].copy()
            for user_id, websocket in user_to_websocket.items():
                if user_id !=sender_id:
                    try:
                        await websocket.send_json(data)
                    except Exception as ex:
                        logging.info(ex)
                        await websocket.close()
                        cls.connections[room_id].pop(user_id)



