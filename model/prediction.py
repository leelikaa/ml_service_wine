from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base, engine
from users import Users


class Prediction(Base):
    __tablename__ = "ptediction"
    prediction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
    user = relationship(Users)
    time = Column(DateTime(timezone=False))
    result = Column(Float)
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



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
