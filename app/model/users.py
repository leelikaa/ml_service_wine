from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database.database import Base, engine


class Users(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    balance = Column(Float)
    email = Column(String)
    telegram = Column(String)
    password = Column(String)
    role = Column(String, CheckConstraint("role IN ('admin', 'regular_user')"), default='regular_user')

    def __str__(self) -> str:
        return self.email


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
