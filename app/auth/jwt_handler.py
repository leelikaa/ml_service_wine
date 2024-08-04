import time
from datetime import datetime
from fastapi import HTTPException, status, Depends
import jwt
from dotenv import load_dotenv
import os
from services.logging_config import get_logger

logger = get_logger(logger_name=__name__)

load_dotenv('.envdb')

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY found in environment variables")


def create_access_token(user_id: str) -> str:
    payload = {
        "user": user_id,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user")
        user_id = int(user_id)
        return user_id
    except jwt.JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
