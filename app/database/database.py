from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from functools import lru_cache
import os
from dotenv import load_dotenv


load_dotenv('.env')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')


if not all([DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME]):
    raise ValueError("One or more database environment variables are missing")

@lru_cache()
def get_db_url() -> str:
    return (
        f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


db_url = get_db_url()

engine = create_engine(url=db_url,
                       echo=False,
                       client_encoding='utf8')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    with SessionLocal() as session:
        return session


def init_db():
    Base.metadata.drop_all(bind=engine) #это на период проверок
    Base.metadata.create_all(bind=engine)
