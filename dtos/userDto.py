import re
import uuid
from typing import List

from pydantic import BaseModel, EmailStr, validator, field_validator
from pydantic.v1 import NoneStr

from entity.userApp import UserApp


class UserDto(BaseModel):
    id:str = None
    username:str = None
    email:str
    password:str
    @classmethod
    def validate_email_format(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError('Invalid email format')


def userDto_to_entity(dto:UserDto)->UserApp:
    if dto.email is None:
        dto.email=dto.username
    dto.validate_email_format()
    return UserApp(id=uuid.uuid4(), username=dto.username, email=dto.email, password=dto.password)
def userEntity_to_Dto(entity:UserApp)->UserDto:
    return UserDto(id=entity.id,username=entity.username,email=entity.email,password="null")

def userListEntity_to_listDto(list_entity:List[UserApp]):
    list_dto=List[UserDto]
    for el in list_entity:
        list_dto.append(userEntity_to_Dto(el))
    return list_dto
