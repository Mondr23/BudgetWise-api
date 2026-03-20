from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth import verify_token
from fastapi import Depends, HTTPException, status




security = HTTPBearer(auto_error=True)


# ---------------------------------------------
# GET CURRENT USER
# ---------------------------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extract user from JWT token
    """

    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = credentials.credentials
    payload = verify_token(token)

    # handle invalid token
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload



# ---------------------------------------------
# REQUIRE ADMIN
# ---------------------------------------------
def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return payload