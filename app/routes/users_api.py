from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from sqlalchemy.orm import Session
from typing import Union
from model.schema import PydanticUsers
from model.users import Users
from services import User_Services, Transaction_Services
from auth.jwt_handler import create_access_token, verify_access_token,oauth2_scheme


user_route = APIRouter(tags=["User"])
hash_password = User_Services.HashPassword()


@user_route.post("/signup")
async def sign_new_user(user: PydanticUsers, session=Depends(get_session)) -> dict:
    user_exist = User_Services.get_user_by_email(user.email, session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already.")

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    User_Services.create_user(user, session)
    return {"message": "User created successfully"}


@user_route.post("/signin")
async def sign_user_in(email: str, password: str, db: Session = Depends(get_session)):
    user_exist = User_Services.get_user_by_email(email, db)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if not hash_password.verify_hash(password, user_exist.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed."
        )
    token = create_access_token(user_exist.user_id)
    print(f"User {email} logged in. Your current balance {user_exist.balance}")
    return {"access_token": token}


@user_route.post("{id}/topup")
def top_up(id: int, money: Union[int, float] = 0.0, db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    money = float(money)
    if money <= 0.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect amount of money, must be >0")
    else:
        Transaction_Services.top_up(id, money, db)
        return {f"Successful top up"}


@user_route.post("{id}/balance")
def user_balance(id: int, db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    verify_access_token(token)
    user = User_Services.get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id not found")
    return user.balance
