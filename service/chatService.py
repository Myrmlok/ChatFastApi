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
        save_chat=await ChatRepository.add(session,chat)
        return await ChatRepository.add_user_to_chat(session,save_chat,user)

    @staticmethod
    @connection
    async def get_chat(chat_id:int,user:UserApp,session)->Chat:
        find_chat=await ChatRepository.find_by_id(session,chat_id)
        if not user in find_chat.users:
            raise UserNotFoundException()
        return find_chat

    @staticmethod
    @connection
    async def update_chat(chat:Chat,user:UserApp,session)->Chat:
        find_chat=await ChatRepository.find_by_id(session,chat.id)
        if not user in find_chat:
            raise UserNotFoundException()
        return await ChatRepository.update_chat(session,chat)

    @staticmethod
    @connection
    async def delete_chat(chat_id:int,user:UserApp,session):
        find_chat=await ChatRepository.find_by_id(session,chat_id)
        if not user in find_chat.users:
            raise  UserNotFoundException()
        await ChatRepository.delete_by_id(session,chat_id)

    @staticmethod
    @connection
    async def add_user_to_chat(chat_id:int,user:UserApp,uuid:UUID,session)->Chat:
        find_user=await UserRepository.find_by_id(session,uuid)
        find_chat=await ChatRepository.find_by_id(session,chat_id)
        if not user in find_chat.users:
            raise UserNotFoundException("user not found in chat")
        return await ChatRepository.add_user_to_chat(session,find_chat,find_user)
