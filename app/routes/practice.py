from fastapi import FastAPI, HTTPException, status, Response , APIRouter
from pydantic import BaseModel
from random import randrange
from app.database import conn, cursor
import time 
from sqlalchemy.orm import Session 
from fastapi import Depends
from .. import models , schema , utils
import psycopg
from app.databaseORM import engine , get_db 

# --------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello! This is me JB 😍😍"}


# @app.get("/posts")
# async def get_posts():
#     return {"data": my_posts}

# @app.get("/posts/{id}")
# async def get_post(id: int):
#     print(id)
#     return {"post_id": id}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": "Success" ,
#             "data": posts}

#Just random endpoints for testing purpose and understanding the endpoints in FastAPI
@router.get("/about")
async def about():
    return {"message": "I am learning FastAPI"}


@router.get("/profile")
async def profile():
    return {
        "name": "Jawad",
        "role": "Frontend Developer"
    }
    
@router.get("/skills")
async def skills():
    return {
        "React",
        "Next JS", 
        'GitHub'
    }

@router.get("/university")
async def university():
    return {
        "name": "COMSATS",
        "Department": "Computer Engineering"
    }

# @router.get("/about")
# async def about():
#     return {
#         "name": "Jawad",
#         "role": "AI Engineer"
#     }
