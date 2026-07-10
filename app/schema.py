from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime
class Post(BaseModel):
    title: str    
    content: str
    published: bool = True
    
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime
    class Config:
        orm_mode = True
        
class LoginUser(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[int] = None
    