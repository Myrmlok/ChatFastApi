from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
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
        await session_db.commit()
        return entity
    @classmethod
    async def get_chat_with_users(cls,session_db:AsyncSession,chat_id:int)->Chat:
        stm= select(Chat).where(Chat.id == chat_id).options(selectinload(Chat.users))
        res=await session_db.execute(stm)
        return res.scalar_one()
    @classmethod
    async def add_user_to_chat(cls,session_db:AsyncSession,chat_id:int, user:UserApp):
        chat=await ChatRepository.get_chat_with_users(session_db,chat_id)
        chat.users.append(user)
        await session_db.commit()

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

