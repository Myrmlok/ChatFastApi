from typing import Tuple

from fastapi import HTTPException

from fastapi.params import Depends
from fastapi.routing import APIRoute, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from dtos.HallDto import HallDto
from dtos.TeamDto import TeamDto
from entity import Team, UserApp, Hall
from entity.Team import TeamRole
from repository.TeamRepository import TeamRepository
from repository.hallRepository import HallRepository
from security.services.authenticateService import get_current_user

team_route=APIRouter(prefix="/teams",tags=["team"])
@team_route.post("/")
async def add_team(dto:TeamDto,user:UserApp=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    team=Team(**(dto.model_dump()))
    res=await TeamRepository.add_with_owner(session,team,user)
    return dto.model_validate(res)
@team_route.get("/{team_id}")
async def get_team(team_id:int,session:AsyncSession=Depends(get_db),user:UserApp=Depends(get_current_user)):
    res:Team= await TeamRepository.find_by_id_with_depends(session,team_id)
    if not  user.id in [el.id for el in res.users]:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not user this team")
    return TeamDto.model_validate(res)






