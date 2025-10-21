import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CONNECTION_STRING: str
    POSTGRES_USERNAME:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    ACCESS_TOKEN_TIME_LIVE:int
    SECRET_KEY: str
    ALGORITHM_HASH: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

settings = Settings()
