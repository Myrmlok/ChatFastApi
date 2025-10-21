from uuid import UUID

from entity.chatEntity import Chat
from entity.userApp import UserApp
from exceptions.UsersExceptions import UserNotFoundException
from repository.userRepository import get_user
from config.db import get_db
from repository.chatRepository import ChatRepository

class ChatService:
    @staticmethod
    def add_chat(chat: Chat, user: UserApp) -> Chat:
        return ChatRepository.add_chat(chat, user)

    @staticmethod
    def get_chat(chat_id:int,user:UserApp)->Chat:
        session_db=get_db()
        find_chat=ChatRepository.get_chat_by_id(chat_id,session_db)
        if not user in find_chat.users:
            raise UserNotFoundException()
        return find_chat

    @staticmethod
    def update_chat(chat:Chat,user:UserApp)->Chat:
        session_db=get_db()
        find_chat=ChatRepository.get_chat_by_id(chat.id,session_db)
        if not user in find_chat:
            raise UserNotFoundException()
        return  ChatRepository.update_chat(chat,session_db)

    @staticmethod
    def delete_chat(chat_id:int,user:UserApp):
        session_db=get_db()
        find_chat=ChatRepository.get_chat_by_id(chat_id,session_db)
        if not user in find_chat.users:
            raise  UserNotFoundException()
        ChatRepository.delete_chat(find_chat,session_db)

    @staticmethod
    def add_user_to_chat(chat_id:int,user:UserApp,uuid:UUID)->Chat:
        session_db=get_db()
        find_user=get_user(uuid,session_db)
        find_chat=ChatRepository.get_chat_by_id(chat_id,session_db)
        if not user in find_chat.users:
            raise UserNotFoundException("user not found in chat")
        return ChatRepository.add_user_to_chat(find_chat,find_user,session_db)
