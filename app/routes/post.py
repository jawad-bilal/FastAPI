from fastapi import FastAPI, HTTPException, status, Response , APIRouter
# from pydantic import BaseModel
# from random import randrange
# from app import models
# from app.database import conn, cursor
# import time 
from sqlalchemy.orm import Session 
from fastapi import Depends
from .. import models , schema , utils
# import psycopg
from app.databaseORM import engine , get_db 

# --------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Posts"] , prefix="/posts")





@router.get("/posts")
async def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("SELECT * FROM post")

    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()

    return {"data": posts}

@router.get("/posts/latest")
async def latest_post():
    return {
        "message": "This is the latest post"
    }

@router.get("/posts/{id}")
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
         post
    }

@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schema.Post , db: Session = Depends(get_db)):

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
       new_post
    }

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/posts/{id}")
async def update_post(id: int, post: schema.Post, db: Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s
    # RETURNING *;""",(post.title,post.content,post.published,id ) ) 
    # updated_post = cursor.fetchone() 
    # conn.commit()

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