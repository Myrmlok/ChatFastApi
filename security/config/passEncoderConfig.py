from passlib.context import CryptContext
from sqlalchemy.util import deprecated

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def get_password_hash(password:str)->str:
    return pwd_context.hash(password)
def verify_password(password:str,password_hash:str)->bool:
    print(password)
    return pwd_context.verify(password,password_hash)