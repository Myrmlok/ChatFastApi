import logging

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import connection
from exceptions.UsersExceptions import UserNotFoundException
from repository.userRepository import UserRepository
from entity.userApp import UserApp
from security.services.jwtService import token_is_valid,token_get_uuid
from service.userService import UserService

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT"
)

async def get_current_user(token:str=Depends(reusable_oauth))->UserApp:
    try:
        if token_is_valid(token) :
            return  await UserService.get_user_by_id(token_get_uuid(token))
    except UserNotFoundException as e:
        print(e.message)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )