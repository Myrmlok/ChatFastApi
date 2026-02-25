from functools import wraps
from inspect import signature

from fastapi import Request, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from watchfiles import awatch

from config.db import connection
from entity import UserApp
from entity.Hall import UserHallRole
from exceptions.UsersExceptions import UserException
from repository.userRepository import UserRepository
from route.UserRoute import user_route
from security.config.OauthConfig import reusable_oauth
from security.services.authenticateService import get_current_user
from security.services.jwtService import token_is_valid, token_get_uuid


def required_auth(user_hall_role:UserHallRole=None,load_user_depends=False,load_hall_depends=False):

    def decorator(method):
        @connection
        @wraps(method)
        async def wrapper(session:AsyncSession,token=Depends(reusable_oauth),*args,**kwargs,):
            current_user:UserApp=None
            try:
                if token_is_valid(token):
                    if not load_user_depends:
                        current_user=await UserRepository.find_by_id(session,token_get_uuid(token))
                    else:
                        current_user=await UserRepository.find_by_id_with_depends(session,token_get_uuid(token))
            except UserException as e:
                print(e.message)
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            setattr(args,"session",session)
            setattr(args,"auth_user",current_user)
            if user_hall_role is None:
                
                return await method(args,kwargs)
            return await  method(args,kwargs)

        return  wrapper
    return  decorator
