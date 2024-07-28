from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_NAME: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    RABBITMQ_USER: Optional[str] = None
    RABBITMQ_PASSWORD: Optional[str] = None

    @property
    def DATABASE_URL(self):
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.envdb')


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
