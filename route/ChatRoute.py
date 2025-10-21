from fastapi import APIRouter, Request, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from dtos.chatDto import ChatDto
from entity.userApp import UserApp
from service.chatService import ChatService
from security.services.authenticateService import get_current_user
chat_route=APIRouter(prefix="/chat")
