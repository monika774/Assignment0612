from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = pwd_context.hash(password)
    new_user = User(email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@auth_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"email": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}