from db.database import SessionLocal
from jose import JWTError

from datetime import timedelta
from fastapi import APIRouter,status,Depends,HTTPException,Security
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from .schemas import UserOut,UserCreate,Token,UserOut,UserLogin
from sqlalchemy.orm import Session
from .utils import verify_password,get_password_hash,decode_access_token,create_access_token,ACCESS_TOKEN_EXPIRY_DURATION
from db.models import User

router=APIRouter(prefix="/auth",tags=["auth"])
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/token")

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

@router.post('/register',response_model=UserOut,status_code=status.HTTP_201_CREATED)
def register(user_in:UserCreate,db:Session=Depends(get_db)):
    user=get_user_by_email(db,user_in.email)
    if user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed=get_password_hash(user_in.password)
    user=User(email=user_in.email,name=user_in.name,password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/token',response_model=Token)
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="couldn't validate credentials")
    expires=timedelta(minutes=ACCESS_TOKEN_EXPIRY_DURATION)
    access_token=create_access_token(user.id,expires)

    return {"access_token":access_token,"token_type":"Bearer"}

@router.post("/token_json",response_model=Token)
def get_access_token_json(user_in:UserLogin,db:Session=Depends(get_db)):
    user=authenticate_user(db,user_in.email,user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="couldn't validate credentials")
    expires=timedelta(minutes=ACCESS_TOKEN_EXPIRY_DURATION)
    access_token=create_access_token(user.id,expires)

    return {"access_token":access_token,"token_type":"Bearer"}



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

@router.get("/me",response_model=UserOut)
def read_own_profile(current_user:User=Depends(get_current_user)):
    return current_user



    


