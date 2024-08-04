from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base, engine
from model.users import Users


class Transaction(Base):
    __tablename__ = "transaction"
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
    user = relationship(Users)
    time = Column(DateTime(timezone=False))  
    money = Column(Float)
    type_ = Column(String)


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
