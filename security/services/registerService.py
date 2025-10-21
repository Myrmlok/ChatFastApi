from sys import exception
from typing import Any

from config.db import get_db
from entity.userApp import UserApp
from repository.userRepository import add_user,get_user_by_email,update_user
from security.config.passEncoderConfig import verify_password,get_password_hash
from exceptions.UsersExceptions import UserAlreadyExistException,UserPasswordNotEquals,UserNotFoundException
def login_user(user:UserApp)->  None | UserApp:
    find_user= get_user_by_email(user.email)
    if find_user is None:
        raise UserNotFoundException(None)
    if not verify_password( user.password,find_user.password):
        raise UserPasswordNotEquals(None)
    return find_user
def register_user(user:UserApp)->UserApp|None:
    db=next(get_db())
    find_user= get_user_by_email(user.email,db)
    if not find_user is None:
        raise UserAlreadyExistException(None)
    user.password=get_password_hash(user.password)
    return  add_user(user,db)

