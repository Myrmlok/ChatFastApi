from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from entity.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from entity.chatEntity import Chat

chat_user_table=Table(
    "chat_user",
    Base.metadata,
    Column("chat_id",ForeignKey("chat.id")),
    Column("user_id",ForeignKey("userApp.id"))
)

class UserApp(Base):
    __tablename__ = "userApp"

    id:Mapped[UUID]=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    email:Mapped[str]=Column(String,unique=True,nullable=False)
    username=Column(String)
    password=Column(String)
    chats:Mapped[List["Chat"]]=relationship(secondary="chat_user",back_populates="users")


