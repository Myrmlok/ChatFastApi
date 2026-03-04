from sys import prefix
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends

from dtos.userDto import UserDto
from entity import UserApp
from security.services.authenticateService import get_current_user
from service.userService import UserService

user_route=APIRouter(prefix="/users",tags=["users"])
@user_route.get("/{user_id}")
async def get_user(user_id:UUID):
    return UserDto.model_validate(await UserService.get_user_by_id(user_id))
@user_route.get("/current/user")
async def get_cur_user(user:UserApp=Depends(get_current_user)):
    return UserDto.model_validate(user)