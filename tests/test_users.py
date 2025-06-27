from app import schemas
from jose import jwt
from app.config import settings
import pytest



def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Social Media App!"}

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "password": "password"
        }
    )
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test@example.com"

def test_login_user(test_user, client):
    response = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ("wrongemail@example.com", "password", 403),
    ("test@example.com", "wrongpassword", 403),
    ("wrongemail@gmail.com","wrongpassword", 403),
])
def test_unauthorized_user(client, username, password, status_code):
    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )
    assert response.status_code == status_code
