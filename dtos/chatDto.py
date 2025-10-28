from typing import List

from pydantic import BaseModel

from dtos.userDto import UserDto
from entity.chatEntity import Chat
from entity.userApp import UserApp
from dtos.userDto import userListEntity_to_listDto

class ChatDto(BaseModel):
    id:int
    name:str
    users:List[UserDto]|None



class ChatMapper:
    @staticmethod
    def entity_to_dto(entity: Chat) -> ChatDto:
        return ChatDto(id=entity.id,name=entity.name,users=userListEntity_to_listDto(entity.users))
    @staticmethod
    def dto_to_entity(dto:ChatDto)->Chat:
        return Chat(id=dto.id,name=dto.name)
