from sqlalchemy import Column, Table, ForeignKey
from config.db import Base


chat_user_table=Table(
    "chat_user",
    Base.metadata,
    Column("chat_id",ForeignKey("chat.id")),
    Column("user_id",ForeignKey("userApp.id"))
)
