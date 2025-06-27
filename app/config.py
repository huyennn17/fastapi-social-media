# import os
# from dotenv import load_dotenv

# env_path = os.path.abspath(".env")
# print("Using .env file at:", env_path)

# load_dotenv(dotenv_path=env_path)
# print("DATABASE_PORT from os:", os.getenv("DATABASE_PORT"))

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
