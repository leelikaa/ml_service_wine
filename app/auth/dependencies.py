from fastapi import Depends, HTTPException, Request, status
from auth.jwt_handler import verify_access_token
from services.logging_config import get_logger
from fastapi.security import OAuth2PasswordBearer

logger = get_logger(logger_name=__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    token = token.removeprefix('Bearer ')
    user = verify_access_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
