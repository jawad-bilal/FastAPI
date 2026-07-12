from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class Post(BaseModel):
    title: str    
    content: str
    published: bool = True
    class config:
        orm_mode = True
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    title: str    
    content: str 
    id: int
    # user_id: int
    published: bool
    created_at : datetime
    owner: UserOut
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
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class VoteOut(BaseModel):
    owner : UserOut
    post : PostOut  
    class Config:
        orm_mode = True
    
    
    