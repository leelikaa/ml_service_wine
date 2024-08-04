from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from sqlalchemy.orm import Session
from typing import Union
from model.schema import PydanticUsers, TokenResponse
from model.users import Users
from services import User_Services, Transaction_Services
from auth.jwt_handler import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import get_current_user
from services.logging_config import get_logger

logger = get_logger(logger_name=__name__)

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


@user_route.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user_exist = User_Services.get_user_by_email(user.username, db)
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    if not hash_password.verify_hash(user.password, user_exist.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed."
        )
    token = create_access_token(str(user_exist.user_id))
#   return(f"User {user.username} logged in. Your current balance {user_exist.balance}")
    return {"access_token": token, "token_type": "Bearer"}


@user_route.post("{id}/topup")
def top_up(id: int, money: Union[int, float] = 0.0, db: Session = Depends(get_session), user: int = Depends(get_current_user)):
    logger.info(f"User from token: {user}")
    if id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. Pls use /user/signin")
    money = float(money)
    if money <= 0.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect amount of money, must be >0")
    else:
        Transaction_Services.top_up(id, money, db)
        return {f"Successful top up"}


@user_route.post("{id}/balance")
def user_balance(id: int, db: Session = Depends(get_session), user: int = Depends(get_current_user)):
    if id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. Pls use /user/signin")
    user = User_Services.get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User id not found")
    return {"balance": user.balance}


@user_route.get("/{username}")
def get_user_id_by_username(username: str, db: Session = Depends(get_session)):
    user = User_Services.get_user_by_email(username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user_id": user.user_id}
