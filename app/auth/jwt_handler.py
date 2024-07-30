import time
from datetime import datetime
from fastapi import HTTPException, status 
import jwt
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer


load_dotenv('.envdb')

SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user_id: str) -> str:
    payload = {
    "user": user_id,
    "expires": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict: 
    try:
        data = jwt.decode(token, SECRET_KEY, 
        algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Token expired!"
            )
        return data
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
