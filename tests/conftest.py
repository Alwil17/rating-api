import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

# Store tokens that need to be shared between test modules
pytest.admin_refresh_token = None
pytest.user_refresh_token = None

@pytest.fixture(scope="session")
def admin_auth():
    """
    Returns a function that can get fresh admin auth headers when needed.
    This is useful when tokens expire during testing.
    """
    def _get_admin_auth():
        admin_payload = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpassword"
        }
        # Try to create admin, ignore if already exists
        client.post("/auth/register", json=admin_payload)
        
        form_data = {
            "username": admin_payload["email"],
            "password": admin_payload["password"]
        }
        response = client.post("/auth/token", data=form_data)
        assert response.status_code == 200, response.text
        token_data = response.json()
        pytest.admin_refresh_token = token_data["refresh_token"]
        return {
            "headers": {"Authorization": f"Bearer {token_data['access_token']}"},
            "refresh_token": token_data["refresh_token"]
        }
    
    return _get_admin_auth


@pytest.fixture(scope="session")
def user_auth():
    """
    Returns a function that can get fresh user auth headers when needed.
    This is useful when tokens expire during testing.
    """
    def _get_user_auth():
        user_payload = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        # Try to create user, ignore if already exists
        client.post("/auth/register", json=user_payload)
        
        form_data = {
            "username": user_payload["email"],
            "password": user_payload["password"]
        }
        response = client.post("/auth/token", data=form_data)
        assert response.status_code == 200, response.text
        token_data = response.json()
        pytest.user_refresh_token = token_data["refresh_token"]
        return {
            "headers": {"Authorization": f"Bearer {token_data['access_token']}"},
            "refresh_token": token_data["refresh_token"]
        }
    
    return _get_user_auth
