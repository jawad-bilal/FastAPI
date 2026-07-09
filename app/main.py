from fastapi import FastAPI, HTTPException, status, Response
# from pydantic import BaseModel
# from random import randrange
# from app.database import conn, cursor
# import time 
from sqlalchemy.orm import Session 
from fastapi import Depends

from app.routes import user , post , auth
from . import models
# import psycopg
from app.databaseORM import engine

# --------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)