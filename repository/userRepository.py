from fastapi.params import Depends

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from entity.userApp import UserApp
from exceptions.UsersExceptions import UserNotFoundException
from repository.crudEntity import CRDEntity


class UserRepository(CRDEntity):
    model=UserApp
    @classmethod
    async def find_by_email(cls,session:AsyncSession,email:str)->UserApp:
        statement=select(UserApp).where(UserApp.email==email)
        find_user=await session.execute(statement)
        return find_user.scalars().first()
    @classmethod
    async def get_user_with_chats(cls, session:AsyncSession, user_id: uuid.UUID)->UserApp:
        stm=select(UserApp).where(UserApp.id==user_id).options(selectinload(UserApp.chats))
        res=await session.execute(stm)
        return res.scalar_one()