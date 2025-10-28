from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer, Identity, Sequence
from sqlalchemy.orm import Mapped, relationship

from entity.base import Base


class Chat(Base):
    __tablename__="chat"

    id=Column(Integer,primary_key=True, server_default=Identity())
    name= Column[String]

    users: Mapped[List["UserApp"]] = relationship(
        secondary="chat_user",
        back_populates="chats",

    )