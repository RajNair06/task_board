from db.database import SessionLocal
from jose import JWTError

from datetime import timedelta
from fastapi import APIRouter,status,Depends,HTTPException,Security
from fastapi.security import OAuth2PasswordRequestForm
from task_board.schemas.auth_schemas import UserOut,UserCreate,Token,UserOut,UserLogin
from sqlalchemy.orm import Session
from task_board.utils.auth_utils import verify_password,get_db,get_user_by_email,authenticate_user,get_password_hash,decode_access_token,create_access_token,ACCESS_TOKEN_EXPIRY_DURATION,get_current_user
from db.models import User
print("get_db id:", id(get_db))


router=APIRouter(prefix="/auth",tags=["auth"])








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





@router.get("/me",response_model=UserOut)
def read_own_profile(current_user:User=Depends(get_current_user)):
    return current_user



    


