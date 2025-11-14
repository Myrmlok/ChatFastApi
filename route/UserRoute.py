from sys import prefix
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends

from dtos.chatDto import ChatMapper
from dtos.userDto import userEntity_to_Dto
from security.services.authenticateService import get_current_user
from service.userService import UserService

user_route=APIRouter(prefix="/users",tags=["users"])
@user_route.get("/{user_id}")
async def get_user(user_id:UUID):
    return userEntity_to_Dto(await UserService.get_user_by_id(user_id))
@user_route.get("/current/user/chats")
async def get_chats(user=Depends(get_current_user)):
    return ChatMapper.listEntity_to_ListDto(await UserService.getChats(user))
@user_route.get("/current/user")
async def get_cur_user(user=Depends(get_current_user)):
    return userEntity_to_Dto(user)