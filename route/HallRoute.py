from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import connection, get_db
from dtos.HallDto import HallDto
from entity import UserApp, Hall, Team
from repository.TeamRepository import TeamRepository
from repository.hallRepository import HallRepository
from security.services.authenticateService import get_current_user

hall_route=APIRouter(prefix="/teams/{team_id}/halls",tags=["halls"])

@hall_route.post("/")
async def  add_hall_to_team(team_id:int,dto:HallDto,session:AsyncSession=Depends(get_db),user:UserApp=Depends(get_current_user)):
    team:Team=await TeamRepository.find_by_id_with_depends(session,team_id)
    if not  user.id in [el.id for el in team.owners]:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not user this team")
    hall:Hall=Hall(**dto.model_dump())
    hall.team_id=team.id
    res=await HallRepository.add(session,hall)
    return HallDto.model_validate(res)
@hall_route.get("/{hall_id}")
async def get_hall(team_id:int,
                   hall_id:int,
                   session:AsyncSession=Depends(get_db),
                   user:UserApp=Depends(get_current_user)):
    team: Team = await TeamRepository.find_by_id_with_depends(session, team_id)
    if not user.id in [el.id for el in team.users]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not user this team")
    res: Hall =await HallRepository.find_by_id_with_depends(session,hall_id)
    return HallDto.model_validate(res)