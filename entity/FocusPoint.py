from typing import List

from sqlalchemy import Integer, Identity, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

class FocusPoint(Base):
    __tablename__ = "focus_point"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, server_default=Identity())
    x:Mapped[float]=mapped_column(Float)
    y:Mapped[float]=mapped_column(Float)
    hall:Mapped["Hall"]=relationship("Hall",back_populates="focusPoints")
    hall_id:Mapped[int]=mapped_column(ForeignKey("hall.id"))
    reports:Mapped[List["Report"]]=relationship("Report",back_populates="focus_point",lazy="selectin")