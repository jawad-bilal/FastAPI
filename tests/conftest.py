import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import OAuth, models
from app.databaseORM import Base, get_db
from app.routes import post, user


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(user.router)
    app.include_router(post.router)
    app.dependency_overrides[get_db] = override_get_db

    def override_get_current_user():
        return models.User(
            id=1,
            email="auth@example.com",
            password="hashed",
            created_at=None,
        )

    app.dependency_overrides[OAuth.get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client, TestingSessionLocal
