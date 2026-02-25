from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import connection
from dtos.HallDto import HallDto
from entity import UserApp, Hall
from repository.hallRepository import HallRepository
from security.decorators.required_auth import required_auth
from security.services.authenticateService import get_current_user

hall_route=APIRouter(prefix="/halls",tags=["halls"])

@hall_route.post("/")
async def add_hall(dto:HallDto,session:AsyncSession,auth_user:UserApp)->HallDto:
    hall:Hall=Hall(**(dto.model_dump(exclude={"vertexes"})))
    hall.user_id=auth_user.id
    return HallDto.model_validate( await  HallRepository.add(session,hall))
