from fastapi import APIRouter, HTTPException, Depends, status
from database.database import SessionLocal
from sqlalchemy.orm import Session

from model.schema import Users
from services import User_Services, Transaction_Services


def get_db():
    with SessionLocal() as db:
        return db


user_router = APIRouter(tags=["User"])
hash_password = User_Services.HashPassword()


@user_router.post("/signup")
async def sign_new_user(user: Users, session=Depends(get_db)) -> dict:
    user_exist = User_Services.get_user_by_email(user.email, session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already.")

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    User_Services.create_user(user, session)

    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_user_in(email: str, password: str, db: Session = Depends(get_db)):
    user_exist = User_Services.get_user_by_email(email, db)

    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if hash_password.verify_hash(password, user_exist.password):
        return {f"User {email} logged in. Your current balance {user_exist.balance}"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )


@user_router.post("{id}/topup")
def top_up(id: int, money: float = 0.0, db: Session = Depends(get_db)):
    if money <= 0.0:
        raise HTTPException(status_code=400, detail="Incorrect amount of money, must be >0")
    else:
        Transaction_Services.top_up(id, money, db)
