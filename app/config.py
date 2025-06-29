# import os
# from dotenv import load_dotenv

# env_path = os.path.abspath(".env")
# print("Using .env file at:", env_path)

# load_dotenv(dotenv_path=env_path)
# print("DATABASE_PORT from os:", os.getenv("DATABASE_PORT"))

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_hostname: str = Field(..., env="DATABASE_HOSTNAME")
    database_port: str = Field(..., env="DATABASE_PORT")
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    database_name: str = Field(..., env="DATABASE_NAME")
    database_username: str = Field(..., env="DATABASE_USERNAME")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"

settings = Settings()
