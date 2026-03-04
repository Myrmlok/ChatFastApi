from typing import List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Integer, Identity, String, ForeignKey, Column, UUID as SQLUUID, Enum, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum as PyEnum
from config.base import Base
from entity.FocusPoint import FocusPoint
from entity.Vertex import Vertex

class Hall(Base):
    __tablename__ = "hall"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, server_default=Identity())
    name:Mapped[str]=mapped_column(String,nullable=False)
    vertexes:Mapped[List[Vertex]]=relationship("Vertex",back_populates="hall",lazy="selectin")
    focusPoints:Mapped[List[FocusPoint]]=relationship("FocusPoint",back_populates="hall",lazy="selectin")
    team_id:Mapped[int]=mapped_column(ForeignKey("team.id"))
    team:Mapped["Team"]=relationship("Team",back_populates="halls")