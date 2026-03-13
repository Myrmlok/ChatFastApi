from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from entity import UserApp
from entity.Team import TeamRole, Team
from repository.TeamRepository import TeamRepository


class CheckAuth:
    @classmethod
    async def check_auth(cls,session:AsyncSession,team_id,user_id,team_role:TeamRole)->Team:


        match team_role:
            case TeamRole.USER:
                team:Team=await TeamRepository.find_by_id_with_users(session,team_id)
                arr=team.users
            case TeamRole.ADMIN:
                team: Team = await TeamRepository.find_by_id_with_admins(session, team_id)
                arr=team.admins
            case TeamRole.OWNER:
                team: Team = await TeamRepository.find_by_id_with_admins(session, team_id)
                arr=team.owners
        for el in arr:
            if el.id==user_id:
                return team
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You have no right this table")
