from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token
from ..utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(username=payload.username, password_hash=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@router.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
