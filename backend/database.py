from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE")
DB_CONNECTION = os.getenv("DB_CONNECTION")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DB_URL = f'{DB_TYPE}+{DB_CONNECTION}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    from backend.models.user import Base as UserBase
    from backend.models.user_session import Base as UserSessionBase
    UserBase.metadata.create_all(bind=engine)
    UserSessionBase.metadata.create_all(bind=engine)