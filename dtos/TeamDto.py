from typing import List

from pydantic import BaseModel, ConfigDict

from dtos.HallDto import HallDto
from dtos.userDto import UserDto


class TeamDto(BaseModel):
    id:int=None
    name:str
    users:List[UserDto]=[]
    admins:List[UserDto]=[]
    owners:List[UserDto]=[]
    halls:List[HallDto]=[]
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
