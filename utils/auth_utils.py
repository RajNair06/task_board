from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
import os
from db.models import User
from sqlalchemy.orm import Session
from db.database import SessionLocal
from dotenv import load_dotenv
load_dotenv()
ALGORITHM='HS256'
SECRET_KEY=os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRY_DURATION=60*24

pwd_context=CryptContext(schemes=["bcrypt"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()

def authenticate_user(db:Session,email:str,password:str):
    user=get_user_by_email(db,email)
    if not user:
        return None
    if not verify_password(password,user.password_hash):
        return None
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(actual_password,hashed_password):
    return pwd_context.verify(actual_password,hashed_password)

def create_access_token(id,expires_time_delta):
    
    if expires_time_delta:
        expire=datetime.now()+expires_time_delta
    else:
        expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_DURATION)
    encode={'id':id,"exp":expire}
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_token(token):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise

    

