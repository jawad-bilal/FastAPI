from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.types import conint


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    published: bool = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    id: int
    created_at: datetime


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    id: int
    published: bool
    created_at: datetime
    owner: UserOut


class PostVote(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Post: PostOut
    votes: int


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class VoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    owner: UserOut
    post: PostOut
    
    
    