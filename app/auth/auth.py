# JWT token creation and verification

from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    """
    Creates JWT token with expiration
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    Verifies token and returns payload
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None