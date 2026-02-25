from typing import List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Integer, Identity, String, ForeignKey, Column, UUID as SQLUUID, Enum, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum as PyEnum
from config.base import Base
from entity.FocusPoint import FocusPoint
from entity.Vertex import Vertex
class UserHallRole(str,PyEnum):
    USER="USER"
    ADMIN="ADMIN"
    OWNER="OWNER"


class TeamHall(Base):
    __tablename__ = "team_hall"

    user_id = Column(SQLUUID(as_uuid=True), ForeignKey("user_app.id"), primary_key=True)
    hall_id = Column(Integer, ForeignKey("hall.id"), primary_key=True)
    role = Column(Enum(UserHallRole), nullable=False, default=UserHallRole.USER)


class Hall(Base):
    __tablename__ = "hall"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, server_default=Identity())
    name:Mapped[str]=mapped_column(String,nullable=False)
    vertexes:Mapped[List[Vertex]]=relationship("Vertex",back_populates="hall",lazy="selectin")
    focusPoints:Mapped[List[FocusPoint]]=relationship("FocusPoint",back_populates="hall",lazy="selectin")
    user:Mapped["UserApp"]=relationship("UserApp",back_populates="halls")
    user_id:Mapped[UUID]=mapped_column(ForeignKey("user_app.id"))