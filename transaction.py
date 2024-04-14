from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from user import UserGet


class Transaction(Base):
    __tablename__ = "transaction"
    #__table_args__ = 
    
    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(user.user_id), primary_key=True)
    user = relationship(UserGet)
    time = Column(DateTime(timezone=False))  
    money = Column(Float)
    type_ = Column(String)
