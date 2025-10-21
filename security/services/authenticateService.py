from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordBearer
from starlette import status

from exceptions.UsersExceptions import UserNotFoundException
from repository.userRepository import get_user
from entity.userApp import UserApp
from security.services.jwtService import token_is_valid,token_get_uuid


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT"
)
def get_current_user(token:str=Depends(reusable_oauth))->UserApp:
    try:
        if token_is_valid(token) :
            return  get_user(token_get_uuid(token))
    except UserNotFoundException as e:
        print(e.message)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
