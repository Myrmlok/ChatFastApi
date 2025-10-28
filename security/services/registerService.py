from sys import exception
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from config.db import connection
from entity.userApp import UserApp
from repository.userRepository import UserRepository
from security.config.passEncoderConfig import verify_password,get_password_hash
from exceptions.UsersExceptions import UserAlreadyExistException,UserPasswordNotEquals,UserNotFoundException
class RegisterService:
    @staticmethod
    @connection
    async def login_user(user:UserApp,session)->  None | UserApp:
        find_user=await UserRepository.find_by_email(session,user.email)
        if find_user is None:
            raise UserNotFoundException(None)
        if not verify_password( user.password,find_user.password):
            raise UserPasswordNotEquals(None)
        return find_user
    @staticmethod
    @connection
    async def register_user(user:UserApp,session)->UserApp|None:
        user.password=get_password_hash(user.password)
        try:
            res=await  UserRepository.add(session,user)
            return res
        except SQLAlchemy as e:
            raise UserAlreadyExistException()


