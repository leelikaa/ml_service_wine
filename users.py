from sqlalchemy import Column, Integer, String, Float
from database import Base


class UserGet(Base):
    __tablename__ = "user"
    #__table_args__ = 
    
    user_id = Column(Integer, primary_key=True)
    balance = Column(Float)
    email = Column(String)
    password Column(String)
    gender = Column(String)
    age = Column(Integer)
    city = Column(String)
    role = Column(String) 