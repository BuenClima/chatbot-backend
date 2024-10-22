from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.configuration import ACCESS_JWT_SECRET, ALGORITHM, REFRESH_JWT_SECRET
import app.users.crud as users
from app.users.schemas import User
from app.core.database import get_db
from app.core.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get the current user.

    :param token: JWT token
    :type token: str
    :param db: Database session
    :type db: Session
    :return: User object
    :rtype: User
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = users.get_user_by_id(db, user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as exc:
        logger.error("Error decoding token: %s", exc)
        raise credentials_exception from exc

def get_current_user_refresh(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Get the current user using a refresh token.

    :param token: JWT refresh token
    :type token: str
    :param db: Database session
    :type db: Session
    :return: User object
    :rtype: User
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, REFRESH_JWT_SECRET, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = users.get_user_by_id(db, user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as exc:
        logger.error("Error decoding token: %s", exc)
        raise credentials_exception from exc
