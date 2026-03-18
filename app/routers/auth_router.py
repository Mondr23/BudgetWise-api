from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.auth.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["sha256_crypt"])

# TEMP users (later you can move to database)
users = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": pwd_context.hash("user123"),
        "role": "user"
    }
}


@router.post("/login")
def login(username: str, password: str):
    """
    Login endpoint → returns JWT token
    """

    user = users.get(username)

    # check username + password
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # create token with role
    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": token}