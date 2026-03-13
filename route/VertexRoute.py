from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from dtos.VertexDto import VertexDto
from entity import UserApp, Hall, Vertex, Team
from entity.Team import TeamRole
from repository.TeamRepository import TeamRepository
from repository.VertexRepository import VertexRepository
from repository.hallRepository import HallRepository
from route.HallRoute import get_hall
from security.checks.check_auth import CheckAuth
from security.services.authenticateService import get_current_user, get_current_user_id

vertex_point_router=APIRouter(prefix="/teams/{team_id}/halls/{hall_id}/vertexes",tags=["vertex"])
@vertex_point_router.post("/")
async def add_vertex(
        team_id:int,
        hall_id:int,
        dto:VertexDto,
        session:AsyncSession=Depends(get_db),
        user_id=Depends(get_current_user_id)):
    await CheckAuth.check_auth(session,team_id,user_id,TeamRole.ADMIN)
    vertex:Vertex=Vertex(**dto.model_dump())
    vertex.hall_id=hall_id
    res=await VertexRepository.add(session,vertex)
    return res