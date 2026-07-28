import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.presentation.dependencies import get_user_repository
from app.auth.infrastructure.memory_repository import InMemoryUserRepository

@pytest.fixture
def test_repo():
    repo = InMemoryUserRepository()
    return repo

@pytest.fixture
def client(test_repo):
    # Override the global dependency with a fresh instance per test
    app.dependency_overrides[get_user_repository] = lambda: test_repo
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_successful_registration(client):
    response = client.post("/auth/register", json={
        "username": "johndoe",
        "email": "john@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "john@example.com"
    assert "password_hash" not in data
    assert "password" not in data
    assert "id" in data
    assert data["is_active"] is True

def test_duplicate_email_rejection(client):
    payload = {
        "username": "userone",
        "email": "duplicate@example.com",
        "password": "strongpassword123"
    }
    client.post("/auth/register", json=payload)
    
    # Attempt duplicate
    payload["username"] = "usertwo"
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert "Email is already registered" in response.json()["detail"]

def test_duplicate_username_rejection(client):
    payload = {
        "username": "duplicateuser",
        "email": "userone@example.com",
        "password": "strongpassword123"
    }
    client.post("/auth/register", json=payload)
    
    # Attempt duplicate
    payload["email"] = "usertwo@example.com"
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert "Username is already taken" in response.json()["detail"]

def test_successful_login(client):
    # Register first
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "strongpassword123"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_login_incorrect_password_rejection(client):
    client.post("/auth/register", json={
        "username": "badpass",
        "email": "badpass@example.com",
        "password": "strongpassword123"
    })
    
    response = client.post("/auth/login", json={
        "email": "badpass@example.com",
        "password": "wrongpassword!"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_login_unknown_email_rejection(client):
    response = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]
