from fastapi.security import OAuth2PasswordBearer

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT"
)
