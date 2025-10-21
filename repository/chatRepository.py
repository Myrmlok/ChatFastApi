from flask import session
from config.db import get_db
from entity.chatEntity import Chat
from entity.userApp import UserApp
from exceptions.EntityException import EntityException
class ChatRepository:
    @staticmethod
    def add_chat(entity:Chat,user:UserApp,session_db=next(get_db()))->Chat:
        user.chats.append(entity);
        session_db.commit()
        session_db.refresh(entity)
        return entity
    @staticmethod
    def get_chat_by_id(id:int, session_db=next(get_db()))->Chat:
        find_chat=session_db.get(Chat, id)
        if find_chat is None:
            raise EntityException("chat not found",Chat)
        return find_chat
    @staticmethod
    def update_chat(entity:Chat, session_db=next(get_db()))->Chat:
        find_chat=ChatRepository.get_chat_by_id(entity.id)
        find_chat.name=entity.name
        session_db.commit()
        session_db.refresh(find_chat)
        return find_chat
    @staticmethod
    def delete_chat(chat:Chat, session_db=next(get_db())):
        session_db.delete(chat)
        session_db.commit()
    @staticmethod
    def add_user_to_chat(chat:Chat, user:UserApp, session_db=next(get_db()))->Chat:
        chat.users.append(user)
        session_db.commit()
        session_db.refresh(chat)
        return chat
    @staticmethod
    def delete_user_to_chat(chat:Chat,user:UserApp,session_db=next(get_db()))->Chat:
        chat.users.remove(user)
        session_db.commit()
        session_db.refresh(chat)
        return chat

