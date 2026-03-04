from functools import wraps
from inspect import signature
from typing import List, Any, Coroutine, Tuple

from fastapi import Request, Depends, HTTPException, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from config.db import connection, get_db
from entity import UserApp, Team
from entity.Team import TeamRole, Team
from exceptions.UsersExceptions import UserException
from repository.TeamRepository import TeamRepository
from repository.userRepository import UserRepository
from route.UserRoute import user_route
from security.config.OauthConfig import reusable_oauth
from security.services.authenticateService import get_current_user
from security.services.jwtService import token_is_valid, token_get_uuid
