from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from entity import Team, UserApp
from entity.Team import TeamAssociation, TeamRole
from repository.crudEntity import CRDEntity


class TeamRepository(CRDEntity):
    model = Team
    @classmethod
    async def add_with_owner(cls,session:AsyncSession,team:Team,owner:UserApp)->Team:
        session.add(team)
        await session.flush()
        stmt=insert(TeamAssociation).values(
            team_id=team.id,
            user_id=owner.id,
            role=TeamRole.OWNER
        )
        await session.execute(stmt)
        await session.commit()
        res = await cls.find_by_id_with_depends(session, team.id)
        return res
    @classmethod
    async def add_user(cls,session:AsyncSession,team:Team,user:UserApp,role:TeamRole)->Team:
        stmt=insert(TeamAssociation).values(
            team_id=team.id,
            user_id=user.id,
            role=role
        )
        await session.execute(stmt)
        await session.commit()
        res= await cls.find_by_id_with_depends(session,team.id)
        return res
    @classmethod
    async def find_by_id_with_depends(cls,session:AsyncSession,model_id)->Team|None:
        return await cls.find_by_id_with_select_depends(session,model_id,
                                                  selectinload(Team.users),
                                                  selectinload(Team.admins),
                                                  selectinload(Team.owners))
    @classmethod
    async def find_by_id_with_users(cls,session:AsyncSession,model_id)->Team|None:
        return await cls.find_by_id_with_select_depends(session,model_id,
                                                        selectinload(Team.users))
    @classmethod
    async def find_by_id_with_admins(cls,session:AsyncSession,model_id)->Team|None:
        return await cls.find_by_id_with_select_depends(session, model_id,
                                                        selectinload(Team.admins))

    @classmethod
    async def find_by_id_with_owners(cls, session: AsyncSession, model_id)->Team|None:
        return await cls.find_by_id_with_select_depends(session, model_id,
                                                        selectinload(Team.owners))

