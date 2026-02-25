from typing import List

from pydantic import BaseModel

from dtos.ReportDto import ReportDto


class FocusPointDto(BaseModel):
    id: int=None
    x: float
    y:float
    hall_id: int
    reports:List[ReportDto]=[]

