from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session


from .. import models, schema, utils
from app.databaseORM import  get_db

router = APIRouter(tags=["Authentication"] , prefix="/auth")

@router.post("/login")
async def login(user_credentials: schema.LoginUser, db: Session = Depends(get_db)):
    # Step 1: Check if the user exists in the database
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    verify_password = utils.verify(user_credentials.password, user.password)
    # Step 2: Verify the password
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    # Step 3: If credentials are valid, return a success message
    return {"Login successful!"}