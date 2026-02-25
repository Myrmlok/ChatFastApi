from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Table

from dtos.FocusPointDto import FocusPointDto
from dtos.VertexDto import VertexDto


class HallDto(BaseModel):
    id:int=None
    name:str
    user_id:UUID=None
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
    vertexes:List[VertexDto]=[]
    focusPoints:List[FocusPointDto]=[]

