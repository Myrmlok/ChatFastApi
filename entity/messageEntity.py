import datetime


from sqlalchemy import String,  Identity, DateTime, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column


from sqlalchemy import  Integer, ForeignKey, UUID

from config.base import Base

class MessageEntity(Base):
    __tablename__ = "message"
    id:Mapped[int]=mapped_column(Integer,primary_key=True, server_default=Identity())
    text:Mapped[str]=mapped_column(String,nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    sender_id:Mapped[UUID]=mapped_column(ForeignKey("user_app.id"))
    chat_id:Mapped[int]=mapped_column(ForeignKey("chat.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    def __iter__(self):
        yield 'text',self.text
        yield 'created_at',self.created_at
        yield 'chat_id',self.chat_id
        yield 'sender_id',self.sender_id
