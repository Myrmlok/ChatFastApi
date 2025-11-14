import uuid
from sys import exception
from typing import Any, Dict, List
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.instrumentation import find_native_user_instrumentation_hook
from sqlalchemy.util import await_only

from config.db import connection
from config.envApp import settings
from entity.userApp import UserApp
from repository.userRepository import UserRepository
from security.config.passEncoderConfig import verify_password,get_password_hash
from exceptions.UsersExceptions import UserAlreadyExistException, UserPasswordNotEquals, UserNotFoundException, \
    UserException
from service.emailService import EmailService


class RegisterService:
    usersWaitedApproved= {}
    @classmethod
    @connection
    async def login_user(cls,user:UserApp,session)->  None | UserApp:
        find_user=await UserRepository.find_by_email(session,user.email)
        if find_user is None:
            raise UserNotFoundException(None)
        if not verify_password( user.password,find_user.password):
            raise UserPasswordNotEquals(None)
        return find_user
    @classmethod
    @connection
    async def register_user(cls,user:UserApp,session)->UserApp|None:
        find_user=await UserRepository.find_by_email(session,user.email)
        if not find_user is None:
            raise UserAlreadyExistException()
        user.id=uuid.uuid4()
        user.password=get_password_hash(user.password)
        success=await EmailService.async_send_message(user.email,
                                              "Register for chat",
                                              "http://"+settings.EXTERNAL_HOST+"/auth/confirmEmail/"+str(user.id));
        if not success:
            raise UserException("email not valid")
        cls.usersWaitedApproved[user.id]=user
        return user
    @classmethod
    @connection
    async def confirmEmail(cls,user_id:UUID,session)->UserApp:
        find_user=cls.usersWaitedApproved[user_id]
        if not find_user is None:
            return await UserRepository.add(session,find_user)
        raise UserNotFoundException()




