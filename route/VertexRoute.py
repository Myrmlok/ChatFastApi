from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from dtos.VertexDto import VertexDto
from entity import UserApp, Hall, Vertex, Team
from repository.TeamRepository import TeamRepository
from repository.VertexRepository import VertexRepository
from repository.hallRepository import HallRepository
from route.HallRoute import get_hall
from security.services.authenticateService import get_current_user

vertex_point_router=APIRouter(prefix="/teams/{team_id}/halls/{hall_id}/vertexes",tags=["vertex"])
@vertex_point_router.post("/")
async def add_vertex(
        team_id:int,
        hall_id:int,
        dto:VertexDto,
        session:AsyncSession=Depends(get_db),
        user:UserApp=Depends(get_current_user)):
    team: Team = await TeamRepository.find_by_id_with_depends(session, team_id)
    if not user.id in [el.id for el in team.owners]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You not user this team")
    hall: Hall = await HallRepository.find_by_id_with_depends(session, hall_id)
    vertex:Vertex=Vertex(**dto.model_dump())
    vertex.hall_id=hall.id
    res=await VertexRepository.add(session,vertex)
    return res