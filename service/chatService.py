from uuid import UUID

from sqlalchemy.util import await_only

from config.db import connection
from entity.chatEntity import Chat
from entity.userApp import UserApp
from exceptions.UsersExceptions import UserNotFoundException
from repository.userRepository import UserRepository
from repository.chatRepository import ChatRepository

class ChatService:
    @staticmethod
    @connection
    async def add_chat(chat: Chat, user: UserApp,session) -> Chat:
        res=await ChatRepository.add(session,chat)
        return await ChatRepository.add_user_to_chat(session,res.id,user)


    @staticmethod
    @connection
    async def get_chat(chat_id:int,user:UserApp,session)->Chat:
        find_chat=await ChatRepository.get_chat_with_users(session,chat_id)
        if any(user.id==el.id for el in find_chat.users):
            raise UserNotFoundException()
        return find_chat

    @staticmethod
    @connection
    async def update_chat(chat:Chat,user:UserApp,session)->Chat:
        find_chat=await ChatRepository.get_chat_with_users(session,chat.id)
        if not any(user.id==el.id for el in find_chat.users):
            raise UserNotFoundException()
        find_chat.chatName=chat.chatName
        return await ChatRepository.update_chat(session,chat)

    @staticmethod
    @connection
    async def delete_chat(chat_id:int,user:UserApp,session):
        find_chat=await ChatRepository.get_chat_with_users(session,chat_id)
        if not (any(user.id==el.id for el in find_chat.users)):
            raise  UserNotFoundException()
        await ChatRepository.delete_by_id(session,chat_id)
    @staticmethod
    @connection
    async def add_user_to_chat(chat_id:int,user:UserApp,uuid:UUID,session)->Chat:
        find_user=await UserRepository.find_by_id(session,uuid)
        find_chat=await ChatRepository.get_chat_with_users(session,chat_id)
        if not (any(user.id == el.id for el in find_chat.users)):
            raise UserNotFoundException()
        return await ChatRepository.add_user_to_chat(session,find_chat.id,find_user)
