from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import mysql.connector
#import time
from .config import settings 

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         con = mysql.connector.connect(
#             host="localhost", user="root", password="password", database="fastapi")
#         cursor = con.cursor()
#         print("Database connection successful")
#         break
#     except mysql.connector.Error as err:
#         print("Database connection failed")
#         print(f"Error: {err}")
#         time.sleep(2)

