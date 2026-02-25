from typing import List

from pydantic import BaseModel

from dtos.ReportDto import ReportDto


class FocusPoint(BaseModel):
    id: int|None
    x: float
    y:float
    hall_id: int
    reports:List[ReportDto]|None

