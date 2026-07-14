from fastapi import FastAPI, middleware
from app.routes import user , post , practice, vote
from .routes import auth
from . import models
from app.databaseORM import engine
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from random import randrange
# from app.database import conn, cursor
# import time 
# from sqlalchemy.orm import Session 
# from fastapi import Depends
# import psycopg

# --------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],) 
    
    
    
    
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(practice.router)