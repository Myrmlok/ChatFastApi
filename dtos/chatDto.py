from typing import List

from pydantic import BaseModel

from dtos.userDto import UserDto
from entity.chatEntity import Chat
from entity.userApp import UserApp
from dtos.userDto import userListEntity_to_listDto

class ChatDto(BaseModel):
    id:int=None
    name:str
    users:List[UserDto]=None



class ChatMapper:
    @staticmethod
    def entity_to_dto(entity: Chat) -> ChatDto:
        return ChatDto(id=entity.id, name=entity.chatName)
    @staticmethod
    def dto_to_entity(dto:ChatDto)->Chat:
        return Chat(id=dto.id,chatName=dto.name)
    @staticmethod
    def entity_to_dto_withDepends(entity:Chat)->ChatDto:
        return ChatDto(id=entity.id, name=entity.chatName, users=userListEntity_to_listDto(entity.users))
    @staticmethod
    def listEntity_to_ListDto(list_entity:List[Chat])->List[ChatDto]:
        res=[]
        for e in list_entity:
            res.append(ChatMapper.entity_to_dto(e))
        return res