from fastapi import APIRouter

from .. import models
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
