import pytest
import random
import string
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def generate_random_email():
    """Generate a random email to avoid conflicts in tests"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_str}@example.com"

def test_auth_flow():
    # 1. Register a new user with a unique email
    register_payload = {
        "name": "Auth Test User",
        "email": generate_random_email(),
        "password": "authtestpassword"
    }
    response = client.post("/auth/register", json=register_payload)
    assert response.status_code == 201, response.text
    
    # 2. Login to get tokens
    form_data = {
        "username": register_payload["email"],
        "password": register_payload["password"]
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200, response.text
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    
    # 3. Use access token to access protected endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["email"] == register_payload["email"]
    
    # 4. Refresh the token
    refresh_payload = {"refresh_token": refresh_token}
    response = client.post("/auth/refresh", json=refresh_payload)
    assert response.status_code == 200, response.text
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens
    assert new_tokens["refresh_token"] != refresh_token
    
    # 5. Old refresh token should no longer work
    response = client.post("/auth/refresh", json=refresh_payload)
    assert response.status_code == 401, response.text
    
    # 6. Logout
    logout_payload = {"refresh_token": new_tokens["refresh_token"]}
    response = client.post("/auth/logout", json=logout_payload)
    assert response.status_code == 204, response.text
    
    # 7. Refresh token should no longer work after logout
    response = client.post("/auth/refresh", json=logout_payload)
    assert response.status_code == 401, response.text


def test_invalid_refresh_token():
    # Test with an invalid refresh token
    refresh_payload = {"refresh_token": "this_is_not_a_valid_refresh_token"}
    response = client.post("/auth/refresh", json=refresh_payload)
    assert response.status_code == 401, response.text


def test_invalid_login():
    # Test with invalid credentials
    form_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 401, response.text
