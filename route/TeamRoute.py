from fastapi.params import Depends
from fastapi.routing import APIRoute, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from dtos.TeamDto import TeamDto
from entity import Team, UserApp
from repository.TeamRepository import TeamRepository
from security.services.authenticateService import get_current_user

team_route=APIRouter(prefix="/teams",tags=["team"])
@team_route.post("/")
async def add_team(dto:TeamDto,user:UserApp=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    team=Team(**(dto.model_dump()))
    team.owners.append(user)
    return dto.model_validate(await TeamRepository.add(session,team))