from model.users import Users
from typing import List
from passlib.context import CryptContext


def get_all_users(session) -> List[Users]:
    return session.query(Users).all()


def get_user_by_id(user_id: int, session) -> Users:
    users = session.query(Users).filter(Users.user_id == user_id).first()
    if users:
        return users
    return None


def get_user_by_email(email: str, session) -> Users:
    users = session.query(Users).filter(Users.email == email).first()
    if users:
        return users
    return None


def create_user(user: Users, session) -> None:
    new_user = Users(email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
