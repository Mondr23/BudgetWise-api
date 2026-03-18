# Handles authentication + role checking

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth import verify_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extract user from token
    """

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def require_admin(user: dict):
    """
    Only allow admin
    """

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")