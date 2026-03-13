from sys import prefix
from uuid import UUID

from alembic.script.revision import DependencyLoopDetected
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from dtos.userDto import UserDto
from entity import UserApp
from repository.userRepository import UserRepository
from security.services.authenticateService import get_current_user, get_current_user_id
from service.userService import UserService

user_route=APIRouter(prefix="/users",tags=["users"])
@user_route.get("/{user_id}")
async def get_user(user_id:UUID)->UserDto:
    return UserDto.model_validate(await UserService.get_user_by_id(user_id))
@user_route.get("/current/user")
async def get_cur_user(session:AsyncSession=Depends(get_db),user_id:UUID=Depends(get_current_user_id))->UserDto:
    user:UserApp=await UserRepository.find_by_id_with_depends(session,user_id)
    return UserDto.model_validate(user)