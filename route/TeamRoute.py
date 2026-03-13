from typing import Tuple
from uuid import UUID

from fastapi import HTTPException

from fastapi.params import Depends
from fastapi.routing import APIRoute, APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db import get_db
from dtos.HallDto import HallDto
from dtos.TeamDto import TeamDto
from entity import Team, UserApp, Hall
from entity.Team import TeamRole
from repository.TeamRepository import TeamRepository
from repository.hallRepository import HallRepository
from repository.userRepository import UserRepository
from security.checks.check_auth import CheckAuth
from security.services.authenticateService import get_current_user, get_current_user_id

team_route=APIRouter(prefix="/teams",tags=["team"])
@team_route.post("/")
async def add_team(dto:TeamDto,
                   user:UserApp=Depends(get_current_user),
                   session:AsyncSession=Depends(get_db))->TeamDto:
    team=Team(**(dto.model_dump()))
    res=await TeamRepository.add_with_owner(session,team,user)
    return dto.model_validate(res)
@team_route.get("/{team_id}")
async def get_team(team_id:int,
                   session:AsyncSession=Depends(get_db),
                   user_id:UUID=Depends(get_current_user_id))->TeamDto:
    await CheckAuth.check_auth(session,team_id,user_id,TeamRole.USER)
    res: Team =await TeamRepository.find_by_id_with_depends(session,team_id)
    return TeamDto.model_validate(res)
@team_route.post("/{team_id/users/{new_user_id}")
async def add_user_to_team(team_id:int,
                           new_user_id:UUID,
                           session:AsyncSession=Depends(get_db),
                           owner_id:UUID=Depends(get_current_user_id))->TeamDto:
    team:Team=await CheckAuth.check_auth(session,team_id,owner_id,TeamRole.OWNER)
    new_user:UserApp=await UserRepository.find_by_id(session,new_user_id)
    res:Team=await TeamRepository.add_user(session,team,new_user,TeamRole.USER)
    return TeamDto.model_validate(res)
@team_route.post("/{team_id/admins/{new_admin_id}")
async def add_admin_to_team(team_id:int,
                           new_admin_id:UUID,
                           session:AsyncSession=Depends(get_db),
                           owner_id:UUID=Depends(get_current_user_id))->TeamDto:
    team:Team=await CheckAuth.check_auth(session,team_id,owner_id,TeamRole.OWNER)
    new_admin:UserApp=await UserRepository.find_by_id(session,new_admin_id)
    res:Team=await TeamRepository.add_user(session,team,new_admin,TeamRole.ADMIN)
    return TeamDto.model_validate(res)
@team_route.post("/{team_id/owners/{new_owner_id}")
async def add_admin_to_team(team_id:int,
                           new_owner_id:UUID,
                           session:AsyncSession=Depends(get_db),
                           owner_id:UUID=Depends(get_current_user_id))->TeamDto:
    team:Team=await CheckAuth.check_auth(session,team_id,owner_id,TeamRole.OWNER)
    new_owner:UserApp=await UserRepository.find_by_id(session,new_owner_id)
    res:Team=await TeamRepository.add_user(session,team,new_owner,TeamRole.OWNER)
    return TeamDto.model_validate(res)
@team_route.get("/{team_id}/right")
async def get_right(team_id:int,
                    session: AsyncSession = Depends(get_db),
                    user_id:UUID=Depends(get_current_user_id)):
    team:Team=await TeamRepository.find_by_id_with_depends(session,team_id)
    if user_id in [el.id for el in team.owners]:
        return TeamRole.OWNER
    if user_id in [el.id for el in team.admins]:
        return TeamRole.ADMIN
    if user_id in [el.id for el in team.users]:
        return TeamRole.USER
    return "you have not any rights to this table"





