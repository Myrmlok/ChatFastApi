from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from dtos.FocusPointDto import FocusPointDto
from dtos.HallDto import HallDto
from entity import UserApp, Hall, FocusPoint, Team
from repository.FocusPointRepository import FocusPointRepository
from repository.TeamRepository import TeamRepository
from repository.hallRepository import HallRepository
from route.HallRoute import get_hall
from security.services.authenticateService import get_current_user

focus_point_route=APIRouter(prefix="/teams/{team_id}/halls/{hall_id}/focus_points",tags=["focus_point"])
@focus_point_route.post("/")
async def add_focus_point(team_id:int,
                          hall_id:int,
                          focus_dto:FocusPointDto,
                          session:AsyncSession=Depends(get_db),
                          user:UserApp=Depends(get_current_user)):
    team: Team = await TeamRepository.find_by_id_with_depends(session, team_id)
    if not user.id in [el.id for el in team.owners]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not user this team")
    hall: Hall = await HallRepository.find_by_id_with_depends(session, hall_id)
    focus_point:FocusPoint=FocusPoint(**focus_dto.model_dump())
    focus_point.hall_id=hall.id
    res=await FocusPointRepository.add(session,focus_point)
    return FocusPointDto.model_validate(res)