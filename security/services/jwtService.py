import uuid
from datetime import datetime, timedelta
from datetime import timezone


from jose import jwt, JWTError
from pydantic.v1 import UUID4
from sqlalchemy import false

from config.envApp import settings
from entity.userApp import UserApp


def create_access_token(user:UserApp)->str:
    expire=datetime.now(timezone.utc)+timedelta(seconds=settings.ACCESS_TOKEN_TIME_LIVE)
    to_encode={"uuid":str(user.id),"exp":expire}
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM_HASH)
def get_claims(token:str)->dict:
    return jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM_HASH)
def token_get_uuid(token:str)-> uuid.UUID:
    return uuid.UUID(get_claims(token).get("uuid"))
def token_is_valid(token:str)->bool:
    try:
        get_claims(token)
        return True
    except JWTError:
        return False
