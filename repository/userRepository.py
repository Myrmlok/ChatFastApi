from fastapi.params import Depends

from config.db import get_db
import uuid
from entity.userApp import UserApp
from exceptions.UsersExceptions import UserNotFoundException


def add_user(user:UserApp,db=next(get_db()))->UserApp:
    user.id=uuid.uuid4()
    db.add(user)
    db.commit()
    return user
def get_user(id:uuid,db=next(get_db()))->UserApp:
    user= db.get(UserApp,id)
    if user is None:
        raise UserNotFoundException(None)
    return user
def get_user_by_email(email:str,db=next(get_db()))->UserApp:
    return  db.query(UserApp).filter(UserApp.email==email).first()
def update_user(user:UserApp,db=next(get_db()))->UserApp:
    old_user=db.get(UserApp,user.id)
    if old_user is None:
        raise UserNotFoundException(None)
    old_user.username=user.username
    db.commit()
    return db.refresh(old_user)
def delete_user(id:uuid,db=next(get_db())):
    old_user=db.get(UserApp,id)
    if old_user is None:
        raise UserNotFoundException(None)
    db.delete(old_user)
    db.commit()
