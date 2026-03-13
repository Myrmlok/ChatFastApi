from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, foreign, remote
from config.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid



class UserApp(Base):
    __tablename__ = "user_app"
    id:Mapped[UUID]=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email:Mapped[str]=Column(String,unique=True,nullable=False)
    username:Mapped[str]=Column(String,default="user")
    password:Mapped[str]=Column(String)
    teams:Mapped[List["Team"]]=relationship(
        "Team",
        secondary="team_association",
        primaryjoin="UserApp.id==TeamAssociation.user_id",
        secondaryjoin="TeamAssociation.team_id == Team.id",
        lazy="raise",
        viewonly=True,
    )





