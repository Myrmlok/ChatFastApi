import unittest

from entity.userApp import UserApp
from repository.userRepository import add_user,delete_user,update_user,get_user,get_user_by_email


async def test_add():
    user=UserApp()
    user.password="1234"
    user.email="test@mail.ru"
    user.username="dima"
    await add_user(user)


async def test_get_and_delete():
    user=await get_user_by_email("test@mail.ru")
    await delete_user(user.id)


class UserRepositoryTest(unittest.TestCase):
    pass