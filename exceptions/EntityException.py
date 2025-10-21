
from sqlalchemy.orm import DeclarativeBase


class EntityException(Exception):
    def __init__(self,message:str,entity:type[DeclarativeBase]):
        self.message=entity.__name__+":"+message