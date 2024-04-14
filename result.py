from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from prediction import Prediction
from user import UserGet
from transaction import Transaction


class Result(BaseModel):
    __tablename__ = "result"
    #__table_args__ = 
    
    prediction_id = Column(Integer, ForeignKey(prediction.prediction_id), primary_key=True)
    result = relationship(Prediction)
    user_id = Column(Integer, ForeignKey(user.user_id), primary_key=True)
    transaction_id = Column(Integer, ForeignKey(transaction.transaction_id), primary_key=True)