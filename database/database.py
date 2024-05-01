from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


CONNECTIO_URI = config('WINE_DATABASE_URI')

engine = create_engine(CONNECTIO_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
