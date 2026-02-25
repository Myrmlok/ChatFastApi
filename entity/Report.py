from datetime import datetime

from sqlalchemy import Integer, Identity, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base
from entity import FocusPoint


class Report(Base):
    __tablename__ = "report"
    id:Mapped[int]=mapped_column(Integer, primary_key=True, server_default=Identity())
    value:Mapped[str]=mapped_column(String)
    time:Mapped[datetime]=mapped_column(DateTime)
    focus_point:Mapped["FocusPoint"]=relationship("FocusPoint",back_populates="reports")
    focus_point_id:Mapped[int]=mapped_column(ForeignKey("focus_point.id"))