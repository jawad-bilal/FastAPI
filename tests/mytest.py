from app import models
from app.databaseORM import Base


def test_user_model_fields():
    user = models.User(email="test@example.com", password="secret")
    assert user.email == "test@example.com"
    assert user.password == "secret"


def test_post_model_fields():
    post = models.Post(title="Hello", content="World", published=True, user_id=1)
    assert post.title == "Hello"
    assert post.content == "World"
    assert post.published is True
    assert post.user_id == 1


def test_create_user_endpoint(client):
    test_client, _ = client
    payload = {"email": "new@example.com", "password": "password123"}

    response = test_client.post("/users", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == payload["email"]
    assert body["id"] is not None


def test_create_post_endpoint(client):
    test_client, _ = client
    payload = {"title": "My Post", "content": "Body", "published": True}

    response = test_client.post("/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["content"] == payload["content"]
    assert body["published"] is True

