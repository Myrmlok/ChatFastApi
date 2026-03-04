from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

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
        await session.refresh(team,["owners"])
        return team
    @classmethod
    async def add_user(cls,session:AsyncSession,team:Team,user:UserApp,role:TeamRole)->Team:
        stmt=insert(TeamAssociation).values(
            team_id=team.id,
            user_id=user.id,
            role=role
        )
        await session.execute(stmt)
        await session.commit()
        await session.refresh(team)
        return team