from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReportDto(BaseModel):
    id:int|None
    value: str
    time:datetime
    focus_point_id:int
    model_config = ConfigDict(
        from_attributes=True  # автоматическое преобразование из SQLAlchemy
    )
