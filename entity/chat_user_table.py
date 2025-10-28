from sqlalchemy import Column, Table, ForeignKey, Integer
from entity.base import Base
chat_user = Table(
    'chat_user',
    Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user_app.id'), primary_key=True)  # Adjust table name
)