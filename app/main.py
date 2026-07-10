from fastapi import FastAPI
from app.routes import user , post , practice
from .routes import auth
from . import models
from app.databaseORM import engine
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
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(practice.router)