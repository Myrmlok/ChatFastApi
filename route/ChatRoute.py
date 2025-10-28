import uuid
from uuid import UUID

from fastapi import APIRouter, Request, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from dtos.chatDto import ChatDto, ChatMapper
from entity.userApp import UserApp
from service.chatService import ChatService
from security.services.authenticateService import get_current_user

chat_route=APIRouter(prefix="/chats",tags=["chats"])
@chat_route.post("")
async def add_chat(dto:ChatDto,user:UserApp=Depends(get_current_user)):
    return ChatMapper.entity_to_dto(await ChatService.add_chat(ChatMapper.dto_to_entity(dto),user))
@chat_route.get("/{chat_id}")
async def getChat(chat_id:int,user:UserApp=Depends(get_current_user)):
    return await ChatService.get_chat(chat_id,user)
@chat_route.delete("/{chat_id}")
async def delete_chat(chat_id:int,user:UserApp=Depends(get_current_user)):
    await ChatService.delete_chat(chat_id, user)
    return {"message":"ok"}
@chat_route.put("/{chat_id}")
async def update_chat(chat_id:int,dto:ChatDto,user:UserApp=Depends(get_current_user)):
    entity=ChatMapper.dto_to_entity(dto)
    entity.id=chat_id
    await ChatService.update_chat(entity,user)
@chat_route.post("/{chat_id}/users/{user_id}")
def add_user_to_chat(chat_id:int,user_id:str,user:UserApp=Depends(get_current_user)):
    ChatService.add_user_to_chat(chat_id,user,uuid.UUID(user_id))
