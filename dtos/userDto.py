import re
import uuid
from types import NoneType
from typing import List, Any, Self

from pydantic import BaseModel, EmailStr, validator, field_validator, UUID4, ConfigDict, model_validator, Field
from pydantic.v1 import NoneStr

from dtos.HallDto import HallDto
from entity.userApp import UserApp


class UserDto(BaseModel):
    id: uuid.UUID = None
    username:str = None
    email:str
    password:str
    model_config = ConfigDict(
        json_encoders={uuid.UUID: str},
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )

    @model_validator(mode='before')
    @classmethod
    def set_password_to_none(cls, data):
        if hasattr(data, '__dict__') and hasattr(data, 'password'):
            # Для ORM объектов устанавливаем password в None
            data.password = ""
        return data
    def validate_email_format(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex,self.email):
            raise ValueError('Invalid email format')


