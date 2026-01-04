from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
import os
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from db.models import User,BoardMembers,BoardRole
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


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/token")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=decode_access_token(token)
        user_id=int(payload.get("id"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user=db.query(User).get(user_id)
    if not user:
        raise credentials_exception
    return user

    

def require_board_role(user_id,board_id,allowed_roles:set[BoardRole],db:Session=Depends(get_db)):
    member=(db.query(BoardMembers).filter(BoardMembers.user_id==user_id,BoardMembers.board_id==board_id).one_or_none())

    if not member or member.role not in allowed_roles:
        raise HTTPException(status_code=403,detail="insufficient permission")