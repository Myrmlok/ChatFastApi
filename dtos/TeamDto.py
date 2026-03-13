import uuid
from typing import List

from pydantic import BaseModel, ConfigDict

from dtos.HallDto import HallDto
from dtos.userDto import UserDto
class UserModel(BaseModel):
    id: uuid.UUID
    username: str = None
    email: str
    model_config = ConfigDict(
        json_encoders={uuid.UUID: str},
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )

class TeamDto(BaseModel):
    id:int=None
    name:str
    users:List[UserModel]=[]
    admins:List[UserModel]=[]
    owners:List[UserModel]=[]
    halls:List[HallDto]=[]
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
