from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from app.auth.auth import create_access_token
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user or not pwd_context.verify(data.password, user.password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    db.close()
    return {"access_token": token}