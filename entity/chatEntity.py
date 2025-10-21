from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer, Identity, Sequence
from sqlalchemy.orm import Mapped, relationship
from config.db import Base
from entity.userApp import UserApp
from chat_user_table import chat_user_table

class Chat(Base):
    __tablename__="chat"

    id=Column(Integer,primary_key=True, default=Identity())
    name= Column[String]
    users:Mapped[List[UserApp]]=relationship(
        secondary=chat_user_table,back_populates="chats"
    )
