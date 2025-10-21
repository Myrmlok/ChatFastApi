

from fastapi import APIRouter, Request, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import JSONResponse

from dtos.userDto import UserDto
from dtos.userDto import userDto_to_entity
from exceptions.UsersExceptions import UserException
from security.services.registerService import login_user,register_user
from security.services.jwtService import create_access_token

auth_router=APIRouter(prefix="/auth",tags=["auth"])
@auth_router.post("/register")
def register(request_user:UserDto):
    try:
        reg_user= register_user(userDto_to_entity(request_user))
        access_token=create_access_token(reg_user)
    except UserException as e:
        return JSONResponse(content={"message":e.message},status_code=400)
    return {"access_token":access_token,"token_type": "bearer","refresh_token":None}


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    request_user=RequestUser(email=form_data.username,password=form_data.password)
    try:
        log_user =login_user(userDto_to_entity(request_user))
        access_token = create_access_token(log_user)
    except UserException as e:
        return JSONResponse(content={"message:":e.message},status_code=400)
    return {"access_token": access_token, "token_type": "bearer","refresh_token": None}
@auth_router.delete("/logout")
def logout():
    return "not working"
