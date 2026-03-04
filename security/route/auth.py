import logging
from uuid import UUID

from fastapi import APIRouter, Request, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import JSONResponse

from dtos.userDto import UserDto
from entity import UserApp
from exceptions.UsersExceptions import UserException
from security.services.registerService import RegisterService
from security.services.jwtService import create_access_token

auth_router=APIRouter(prefix="/auth",tags=["auth"])
@auth_router.post("/register")
async def register(request_user:UserDto):
    try:
        reg_user=await RegisterService.register_user(UserApp(**(request_user.model_dump())))
        access_token=create_access_token(reg_user)
    except UserException as e:
        return JSONResponse(content={"message":e.message},status_code=400)
    return {"access_token":access_token,"token_type": "bearer","refresh_token":None}


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    request_user=UserDto(email=form_data.username,password=form_data.password)
    try:
        log_user =await RegisterService.login_user(UserApp(**(request_user.model_dump())))
        access_token = create_access_token(log_user)
    except UserException as e:
        return JSONResponse(content={"message:":e.message},status_code=400)
    return {"access_token": access_token, "token_type": "bearer","refresh_token": None}
@auth_router.get("/confirmEmail/{user_id}")
async def confirm_email(user_id:str):
    return UserDto.model_validate(await RegisterService.confirmEmail( UUID(user_id)))
@auth_router.delete("/logout")
def logout():
    return "not working"
