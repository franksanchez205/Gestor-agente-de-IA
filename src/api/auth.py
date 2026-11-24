"""API de autenticación: register, login, me."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.auth.password import hash_password, verify_password
from src.auth.jwt import create_access_token
from src.auth.deps import get_current_user
from src.data.models import User
from src.data.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    nationality: str = "AR"


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = User(
        id=f"u-{req.email}",
        name=req.name,
        email=req.email,
        nationality=req.nationality,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}


@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not user.password_hash or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user