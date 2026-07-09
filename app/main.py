from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
from app.database import conn, cursor
import time 
from sqlalchemy.orm import Session 
from fastapi import Depends
from . import models 
import psycopg
from app.databaseORM import engine , get_db 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
        

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "Success" ,
            "data": posts}

@app.get("/me")
async def root():
    return {"message": "Hello World"}


# @app.get("/posts")
# async def get_posts():
#     return {"data": my_posts}

# @app.get("/posts/{id}")
# async def get_post(id: int):
#     print(id)
#     return {"post_id": id}
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("SELECT * FROM post")

    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()

    return {"data": posts}

@app.get("/posts/latest")
async def latest_post():
    return {
        "message": "This is the latest post"
    }

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """
    #     SELECT * FROM post
    #     WHERE id = %s;
    #     """,
    #     (id,)
    # )

    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    return {
        "data": post
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post , db: Session = Depends(get_db)):

#     cursor.execute(
#     """
#     INSERT INTO post (title, content, published)
#     VALUES (%s, %s, %s)
#     RETURNING *;
#     """,
#     (post.title, post.content, post.published)
# )

#     new_post = cursor.fetchone()

    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "data": new_post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):

        # cursor.execute(
        #     """
        #     DELETE FROM post
        #     WHERE id = %s
        #     RETURNING *;
        #     """,
        #     (id,)
        # )

    #deleted_post = cursor.fetchone()

    #conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )
    
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    
    # cursor.execute( # """ # UPDATE post # SET title = %s, # content = %s, # published = %s # WHERE id = %s # RETURNING *; # """, # ( # post.title, # post.content, # post.published, # id # ) # ) # updated_post = cursor.fetchone() # conn.commit()F

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return {
        "data": post_query.first()
    }
    
#Just random endpoints for testing purpose and understanding the endpoints in FastAPI
@app.get("/about")
async def about():
    return {"message": "I am learning FastAPI"}


@app.get("/profile")
async def profile():
    return {
        "name": "Jawad",
        "role": "Frontend Developer"
    }
    
@app.get("/skills")
async def skills():
    return {
        "React",
        "Next JS", 
        'GitHub'
    }

@app.get("/university")
async def university():
    return {
        "name": "COMSATS",
        "Department": "Computer Engineering"
    }

# @app.get("/about")
# async def about():
#     return {
#         "name": "Jawad",
#         "role": "AI Engineer"
#     }