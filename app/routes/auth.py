from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schema, utils , OAuth
from app.databaseORM import get_db 

router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Step 1: Check if the user exists in the database
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    verify_password = utils.verify(user_credentials.password, user.password)
    # Step 2: Verify the password
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    
    access_token = OAuth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token,
            "token_type": "bearer"}