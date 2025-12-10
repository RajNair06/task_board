from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    name:str
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr

class Token(BaseModel):
    access_token:str
    token_type:str="Bearer"

class TokenData(BaseModel):
    user_id:int|None=None


