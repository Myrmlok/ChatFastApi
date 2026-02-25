from pydantic import BaseModel, ConfigDict

from entity import Vertex


class VertexDto(BaseModel):
    id:int=None
    x:float
    y:float
    hall_id:int
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
