from typing import List

from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from config.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
class UserApp(Base):
    __tablename__ = "userApp"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    email=Column(String,unique=True)
    username=Column(String)
    password=Column(String)
    chats:Mapped[List["Chat"]]=relationship(secondary="chat_user",back_populates="users")


