from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database.database import Base, engine


class Users(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    balance = Column(Float, default=0.0)
    email = Column(String)
    password = Column(String)
    role = Column(String, CheckConstraint("role IN ('admin', 'regular_user')"), default='regular_user')

    def __str__(self) -> str:
        return f"id: {self.id}, email: {self.email}"


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
