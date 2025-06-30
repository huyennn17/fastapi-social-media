import pytest
from app.config import settings
from app.database import get_db, Base
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.main import app
from app.oauth2 import create_access_token

# Override the database URL for testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("SQLAlchemy URL:", SQLALCHEMY_DATABASE_URL)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "password"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    assert new_user["email"] == "test@example.com"
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "abc@gmail.com",
                 "password": "abc123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    from app import models
    post_data = [
        {"title": "Post 1", "content": "Content 1", "owner_id": test_user["id"]},
        {"title": "Post 2", "content": "Content 2", "owner_id": test_user["id"]},
        {"title": "Post 3", "content": "Content 3", "owner_id": test_user["id"]},
        {"title": "Post 4", "content": "Content 4", "owner_id": test_user2["id"]}
    ]
    session.add_all(models.Post(**data) for data in post_data)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
