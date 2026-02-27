from typing import List

from pydantic import BaseModel, ConfigDict

from dtos.HallDto import HallDto
from dtos.userDto import UserDto


class TeamDto(BaseModel):
    id:int=None
    name:str
    members:List[UserDto]=None
    admins_owners:List[UserDto]=None
    owners:List[UserDto]=None
    halls:List[HallDto]=None
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
