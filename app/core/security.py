from datetime import datetime, timedelta,timezone
from typing import Optional
from bcrypt import hashpw, checkpw, gensalt
from jose import jwt
from app.core.configuration import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def get_password_hash(password: str):
    """Generate a hashed password.

    :param password: Password to hash
    :type password: str
    :return: Hashed password
    :rtype: str
    """
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str):
    """Verify a password.

    :param plain_password: Plain password
    :type plain_password: str
    :param hashed_password: Hashed password
    :type hashed_password: str
    :return: True if the password is correct, False otherwise
    :rtype: bool
    """
    return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token.

    :param data: Data to encode in the token
    :type data: dict
    :param expires_delta: Expiry time for the token
    :type expires_delta: Optional[timedelta]
    :return: JWT access token
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
