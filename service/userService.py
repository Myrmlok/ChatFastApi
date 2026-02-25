from uuid import UUID

from config.db import connection
from entity import UserApp
from repository.userRepository import UserRepository


class UserService:
    @staticmethod
    @connection
    async def get_user_by_id(user_id:UUID,session):
        return await UserRepository.find_by_id(session,user_id)