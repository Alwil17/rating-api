import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def admin_auth_headers():
    # Create an admin user and get an authentication token
    create_admin_payload = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpassword"
    }
    response = client.post("/auth/register", json=create_admin_payload)
    if response.status_code != 201:  # If the admin already exists
        assert response.status_code == 400, response.text

    form_data = {
        "username": create_admin_payload["email"],
        "password": create_admin_payload["password"]
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_auth_headers():
    # Create a regular user and get an authentication token
    create_user_payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=create_user_payload)
    if response.status_code != 201:  # If the user already exists
        assert response.status_code == 400, response.text

    form_data = {
        "username": create_user_payload["email"],
        "password": create_user_payload["password"]
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_user(admin_auth_headers):
    # Test creating a new user
    user_payload = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    response = client.post("/users", json=user_payload, headers=admin_auth_headers)
    assert response.status_code == 201, response.text
    created_user = response.json()
    assert created_user["name"] == user_payload["name"]
    assert created_user["email"] == user_payload["email"]


def test_get_user(user_auth_headers):
    # Test retrieving the current user
    response = client.get("/users/1", headers=user_auth_headers)  # Assuming user ID 1
    assert response.status_code == 200, response.text
    user = response.json()
    assert user["id"] == 1
    assert user["email"] == "testuser@example.com"


def test_list_users(admin_auth_headers):
    # Test listing all users (admin-only)
    response = client.get("/users", headers=admin_auth_headers)
    assert response.status_code == 200, response.text
    users = response.json()
    assert len(users) > 0
    assert any(user["email"] == "testuser@example.com" for user in users)


def test_list_user_ratings(user_auth_headers):
    # Test listing ratings for the current user
    response = client.get("/users/1/ratings", headers=user_auth_headers)  # Assuming user ID 1
    assert response.status_code == 200, response.text
    ratings = response.json()
    assert isinstance(ratings, list)


def test_get_recommendations(user_auth_headers):
    # Test getting recommendations for the current user
    response = client.get("/users/1/recommandations", headers=user_auth_headers)  # Assuming user ID 1
    assert response.status_code == 200, response.text
    recommendations = response.json()
    assert isinstance(recommendations, list)


def test_update_user(user_auth_headers):
    # Test updating the current user
    update_payload = {
        "name": "Updated User",
        "email": "updateduser@example.com"
    }
    response = client.put("/auth/edit", json=update_payload, headers=user_auth_headers)  # Assuming user ID 1
    assert response.status_code == 200, response.text
    updated_user = response.json()
    assert updated_user["name"] == update_payload["name"]
    assert updated_user["email"] == update_payload["email"] 


def test_delete_user(admin_auth_headers):
    # Test deleting a user (admin-only)
    response = client.delete("/users/1", headers=admin_auth_headers)  # Assuming user ID 1
    assert response.status_code == 204, response.text

def test_delete_user_self(user_auth_headers):
    # The user deletes their own account via /auth/remove
    response = client.delete("/auth/remove", headers=user_auth_headers)
    assert response.status_code == 204, response.text

    # After deletion, any authenticated request should fail (token is now invalid)
    response = client.get("/users/me", headers=user_auth_headers)
    assert response.status_code in (401, 404, 422)