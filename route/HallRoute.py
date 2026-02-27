from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import connection, get_db
from dtos.HallDto import HallDto
from entity import UserApp, Hall
from repository.hallRepository import HallRepository
from security.services.authenticateService import get_current_user

hall_route=APIRouter(prefix="/halls",tags=["halls"])

@hall_route.post("/")
async def add_hall(dto:HallDto,session:AsyncSession=Depends(get_db),auth_user:UserApp=Depends(get_current_user))->HallDto:
    hall:Hall=Hall(**(dto.model_dump(exclude={"vertexes"})))
    hall.user_id=auth_user.id
    return HallDto.model_validate( await  HallRepository.add(session,hall))
