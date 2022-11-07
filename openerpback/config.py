import os
from pydantic import BaseSettings 

class Settings(BaseSettings):
    SQLITE_SYNC_URL_PREFIX :str = os.getenv("SQLITE_SYNC_URL_PREFIX")
    SQLITE_ASYNC_URL_PREFIX :str = os.getenv("SQLITE_ASYNC_URL_PREFIX")
    POSTGRES_SYNC_URL :str = os.getenv("POSTGRES_SYNC_URL")
    PG_URL :str = os.getenv("PG_URL")
    POSTGRES_ASYNC_URL :str = os.getenv("POSTGRES_ASYNC_URL")
    SECRET_KEY : str = os.getenv("SECRET_KEY")
    JWT_APP_TOKEN_EXPIRE_TIME :int =4
    JWT_REFRESH_TOKEN_EXPIRE_TIME :int =5
    DEBUG : bool=False
    
    class Config:
        env_file = ".env"

settings = Settings()