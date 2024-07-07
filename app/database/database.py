from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional
from pathlib import Path
from pydantic import Field


class Settings(BaseSettings):
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_NAME: Optional[str] = None

    env_file_path: Path = Field(default=Path(__file__).resolve().parent / '.env')

    @property
    def DATABASE_URL(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=str(env_file_path))


@lru_cache()
def get_settings() -> Settings:
    return Settings()


CONNECTIO_URI = get_settings().DATABASE_URL

engine = create_engine(CONNECTIO_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    return session


def init_db():
    Base.metadata.create_all(engine)
