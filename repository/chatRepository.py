from typing import Any, Coroutine

from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import connection
from entity.chatEntity import Chat
from entity.userApp import UserApp
from exceptions.EntityException import EntityException
from repository.crudEntity import CRDEntity


class ChatRepository(CRDEntity):
    model = Chat
    @classmethod
    async def update_chat(cls, session_db:AsyncSession,entity:Chat):
        find_chat= await cls.find_by_id(session_db,entity)
        find_chat.name=entity.name
        try:
            await session_db.commit()
            await session_db.refresh(find_chat)
        except SQLAlchemy as e:
            await session_db.rollback()
            raise e
        return find_chat
    @classmethod
    async def add_user_to_chat(cls,session_db:AsyncSession,chat:Chat, user:UserApp):
        chat.users.append(user)
        try:
            await session_db.commit()
            await session_db.refresh(chat)
        except SQLAlchemy as e:
            await session_db.rollback()
            raise e
        return chat
    @classmethod
    async def delete_user_to_chat(cls,session_db:AsyncSession,chat:Chat,user:UserApp):
        chat.users.remove(user)
        try:
            await session_db.commit()
            await session_db.refresh(chat)
        except SQLAlchemy as e:
            await session_db.rollback()
            raise e
        return chat

