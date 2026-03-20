import os
from dotenv import load_dotenv
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, UTC
from fastapi import HTTPException

# ---------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# ---------------------------------------------
# CREATE TOKEN
# ---------------------------------------------
def create_access_token(data: dict):
    """
    Create JWT token with expiration
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------
# VERIFY TOKEN
# ---------------------------------------------
def verify_token(token: str):
    """
    Decode and validate JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #validate payload structure
        if "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")