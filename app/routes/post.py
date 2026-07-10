from typing import Optional
from fastapi import HTTPException, status, APIRouter
from sqlalchemy.orm import Session 
from fastapi import Depends
from .. import models , schema , OAuth
from app.databaseORM import get_db 
# import psycopg
# from pydantic import BaseModel
# from random import randrange
# from app import models
# from app.database import conn, cursor
# import time 

# --------------------------------------------------------------

router = APIRouter(tags=["Posts"])





@router.get("/posts", response_model=list[schema.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(OAuth.get_current_user), limit : int = 10 , skip : int = 0 , search : str = ""):

    # cursor.execute("SELECT * FROM post")

    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return  posts

@router.get("/posts/latest" , response_model=schema.PostOut)
async def latest_post():
    return {
        "message": "This is the latest post"
    }

@router.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth.get_current_user)):

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
        
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    return {
         post
    }

@router.post("/posts", status_code=status.HTTP_201_CREATED , response_model=schema.PostOut)
async def create_post(post: schema.Post , db: Session = Depends(get_db), current_user: int = Depends(OAuth.get_current_user)):
    


#     cursor.execute(
#     """
#     INSERT INTO post (title, content, published)
#     VALUES (%s, %s, %s)
#     RETURNING *;
#     """,
#     (post.title, post.content, post.published)
# )

#     new_post = cursor.fetchone()

    new_post = models.Post( user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/posts/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth.get_current_user)):

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
    if deleted_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    db.delete(deleted_post)
    db.commit()

    return {deleted_post , f"This post is deleted successfully"}


@router.put("/posts/{id}", response_model=schema.PostOut)
async def update_post(id: int, post: schema.Post, db: Session = Depends(get_db), current_user: int = Depends(OAuth.get_current_user)):
    
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
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return {
        post_query.first()
    }