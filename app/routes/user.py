from fastapi import FastAPI, HTTPException, status, Response , APIRouter
# from pydantic import BaseModel
# from random import randrange
# from app.database import conn, cursor
# import time 
from sqlalchemy.orm import Session 
from fastapi import Depends
from .. import models , schema , utils
# import psycopg
from app.databaseORM import engine , get_db 

# --------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Users"])

# ------------------------------------------------------------------------

# Create a user using SQLAlchemy ORM Endpoint 

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
async def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    
    
    #hash the password --- user password 
    hashed_password = utils.hash(user.password)
    
    
    user.password = hashed_password
    new_user = models.User(
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/user/{id}", response_model=schema.UserOut)
async def get_user(id : int , db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )

    return user