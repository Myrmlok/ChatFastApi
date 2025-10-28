import typing
from typing import Generic

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from entity.base import Base


class CRDEntity:
    model=None
    @classmethod
    async def add(cls,session:AsyncSession,value):
        new_instance=value
        session.add(new_instance)
        try:
            await session.commit()
            await session.refresh(new_instance)
        except SQLAlchemy as e:
            await session.rollback()
            raise e
        return new_instance
    @classmethod
    async def find_by_id(cls,session:AsyncSession,model_id):
        return await session.get(cls.model,model_id)
    @classmethod
    async def delete_by_id(cls,session:AsyncSession,model_id):
        find_model=await cls.find_by_id(session,model_id)
        try:
            await session.delete(find_model)
        except SQLAlchemy as e:
            await  session.rollback()
            raise e



