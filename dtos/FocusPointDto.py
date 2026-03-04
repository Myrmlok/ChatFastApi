from typing import List

from pydantic import BaseModel, ConfigDict

from dtos.ReportDto import ReportDto


class FocusPointDto(BaseModel):
    id: int=None
    x: float
    y:float
    hall_id: int=None
    reports:List[ReportDto]=[]
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )

