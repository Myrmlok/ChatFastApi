from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from config.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from entity.chatEntity import Chat

class UserApp(Base):
    __tablename__ = "user_app"

    id:Mapped[UUID]=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email:Mapped[str]=Column(String,unique=True,nullable=False)
    username=Column(String,default="user")
    password=Column(String)
    chats:Mapped[List["Chat"]]=relationship("Chat",secondary="chat_users",back_populates="users",lazy="selectin")



