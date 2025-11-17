from typing import Dict
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import TokenResponse, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

TOKENS: Dict[str, int] = {}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "USERNAME_TAKEN",
                "message": "username already taken",
                "details": {},
            },
        )
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = str(uuid4())
    TOKENS[token] = user.id
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTH_FAILED",
                "message": "invalid username or password",
                "details": {},
            },
        )
    token = str(uuid4())
    TOKENS[token] = user.id
    return TokenResponse(access_token=token)


def get_current_user(
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "missing or invalid Authorization header",
                "details": {},
            },
        )
    token = authorization.split(" ", 1)[1]
    user_id = TOKENS.get(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "invalid token",
                "details": {},
            },
        )
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "user not found",
                "details": {},
            },
        )
    return user
