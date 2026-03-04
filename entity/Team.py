from enum import Enum as PyEnum
from typing import List

from sqlalchemy import Column, Identity, Integer, String, ForeignKey, Enum, and_, or_
from sqlalchemy.orm import Mapped, relationship, foreign, remote

from config.base import Base

from sqlalchemy import  UUID as SQLUUID

from entity import UserApp, Hall


class TeamRole(str,PyEnum):
    USER="USER"
    ADMIN="ADMIN"
    OWNER="OWNER"


class TeamAssociation(Base):
    __tablename__ = "team_association"
    user_id = Column(SQLUUID(as_uuid=True), ForeignKey("user_app.id"), primary_key=True)
    team_id=  Column(Integer,ForeignKey("team.id"))
    role = Column(Enum(TeamRole), nullable=False, default=TeamRole.USER)

class Team(Base):
    __tablename__ = "team"
    id:Mapped[int]=Column(Integer,primary_key=True,server_default=Identity())
    name:Mapped[str]=Column(String)
    halls:Mapped[List[Hall]]=relationship("Hall",
                                          lazy="selectin",
                                          cascade="save-update, merge, delete",
                                          back_populates="team")
    users:Mapped[List[UserApp]]=relationship(
        "UserApp",
        secondary="team_association",
        primaryjoin=id==foreign(TeamAssociation.team_id),
        secondaryjoin=foreign(TeamAssociation.user_id)==remote(UserApp.id),
        lazy="selectin",
        viewonly=True
    )
    admins: Mapped[List[UserApp]] = relationship(
        "UserApp",
        secondary="team_association",
        primaryjoin=and_(id == foreign(TeamAssociation.team_id),
                         or_(
                             TeamAssociation.role == TeamRole.ADMIN,
                             TeamAssociation.role == TeamRole.OWNER
                         )),
        secondaryjoin=foreign(TeamAssociation.user_id) == remote(UserApp.id),
        viewonly=True,
        lazy="selectin",
        overlaps="users"
    )
    owners: Mapped[List[UserApp]] = relationship(
        "UserApp",
        secondary="team_association",
        primaryjoin=and_(id == foreign(TeamAssociation.team_id),
                         TeamAssociation.role == TeamRole.OWNER),
        viewonly=True,
        secondaryjoin=foreign(TeamAssociation.user_id) == remote(UserApp.id),
        lazy="selectin",
        overlaps="users,admins"
    )

