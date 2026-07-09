from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
from app.database import conn, cursor


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [
    {
        "title": "Title of post 1",
        "content": "Content of post 1",
        "id": 1
    },
    {
        "title": "Favorite Foods 2",
        "content": "I like pizza",
        "id": 2
    }
]

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
async def get_posts():

    cursor.execute("SELECT * FROM post")

    posts = cursor.fetchall()

    return {"data": posts}

@app.get("/posts/latest")
async def latest_post():
    return {
        "message": "This is the latest post"
    }

@app.get("/posts/{id}")
async def get_post(id: int):

    for post in my_posts:
        if post["id"] == id:
            return {"post_detail": post}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post was not found"
)

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):

    cursor.execute(
        """
        INSERT INTO posts (title, content)
        VALUES (%s, %s)
        RETURNING *;
        """,
        (post.title, post.content)
    )

    new_post = cursor.fetchone()

    conn.commit()

    return {
        "data": new_post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    found_index = None

    for index, post in enumerate(my_posts):
        if post["id"] == id:
            found_index = index
            break

    if found_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    my_posts.pop(found_index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):

    found_index = None

    for index, p in enumerate(my_posts):

        if p["id"] == id:

            found_index = index

            break

    if found_index is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found"
        )

    post_dict = post.model_dump()

    post_dict["id"] = id

    my_posts[found_index] = post_dict

    return {
        "data": post_dict
    }

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