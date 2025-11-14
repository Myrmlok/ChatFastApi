from email.policy import default
from typing import List

from pydantic_core.core_schema import nullable_schema
from sqlalchemy import Column, String, Integer, Identity, Nullable
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from config.base import Base
from sqlalchemy import Table, Column, Integer, ForeignKey, UUID

from config.base import Base
chat_user_association = Table(
    'chat_users',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id',ondelete='CASCADE')),
    Column('user_id', UUID, ForeignKey('user_app.id',ondelete='CASCADE'))
)
class Chat(Base):
    __tablename__="chat"

    id:Mapped[int]=mapped_column(Integer,primary_key=True, server_default=Identity())
    chatName:Mapped[str]= mapped_column(String,default="helloChat")

    users: Mapped[List["UserApp"]] = relationship(
        "UserApp",
        secondary=chat_user_association,
        back_populates="chats"

    )
    messages:Mapped[List["MessageEntity"]]=relationship(
        "MessageEntity",
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="MessageEntity.created_at"
    )