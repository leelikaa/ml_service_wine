from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from database import Base
from user import UserGet

class Prediction(Base):
    __tablename__ = "ptediction"
    #__table_args__ = 
   
    prediction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(user.user_id), primary_key=True)
    user = relationship(UserGet)
    fixed_acidity = Column(Float)
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    residual_sugar = Column(Float)
    chlorides = Column(Float)
    free_sulfur_dioxide = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    pH = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    result = Column(Float)