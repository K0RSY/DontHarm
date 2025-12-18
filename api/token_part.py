from models import *
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from password import *
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

SECRET_KEY = "nuhf873whf9uwr9chwog879237279dx7ohw8986y9c6gw38crgyugc6t86wthc8wtc8wtgcg7th7t"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SQLALCHEMY_DATABASE_URL = URL.create(
    "mysql",
    username="root",
    password=DATABASE_PASSWORD,
    host="localhost",
    port=3306,
    database="dont_harm",
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user(db: Session, login: str):
    return db.query(LaboratoryAssistants).filter(LaboratoryAssistants.login == login).first()

def get_user_with_password(db: Session, login: str, password: str):
    return db.query(LaboratoryAssistants).filter(LaboratoryAssistants.login == login, LaboratoryAssistants.password == password).first()

def authenticate_user(db: Session, login: str, password: str):
    user = get_user_with_password(db, login, password)
    if not user:
        return False
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            return None
        token_data = TokenData(login=login)
    except JWTError:
        return None
    user = get_user(db, login=token_data.login)
    if user is None:
        return None
    return user