
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.base import ExecutableOption


class CRDEntity:
    model= None
    @classmethod
    async def add(cls,session:AsyncSession,value):
        new_instance=value
        session.add(new_instance)
        await session.commit()
        await session.refresh(new_instance)
        return new_instance
    @classmethod
    async def find_by_id(cls,session:AsyncSession,model_id):
        return await session.get(cls.model,model_id)
    @classmethod
    async def delete_by_id(cls,session:AsyncSession,model_id):
        find_model=await cls.find_by_id(session,model_id)
        await session.delete(find_model)
        await session.commit()
    @classmethod
    async def find_by_id_with_depends(cls,session:AsyncSession,model_id):
        stmt = select(cls.model).where(cls.model.id == model_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id_with_select_depends(cls, session: AsyncSession, model_id, *options: ExecutableOption):
        query = select(cls.model).options(*options).where(cls.model.id == model_id)
        res = await session.execute(query)
        return res.scalar_one_or_none()

