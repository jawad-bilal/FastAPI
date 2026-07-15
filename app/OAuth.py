from fastapi import Depends, HTTPException , status
from jose import jwt, JWTError
from datetime import datetime, timedelta , timezone
from dotenv import load_dotenv
import os

from app import models
from . import schema , databaseORM
from sqlalchemy.orm import Session 
from app.databaseORM import get_db 

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "test-secret-key"
ALGORITHM = os.getenv("TOKEN_ALGORITHM") or "HS256"
JWT_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES") or 30)

# print(JWT_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id=id)
        
    except JWTError:
        
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = verify_access_token(token, credentials_exception)
    # print(token.id)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # print(user)
    return user