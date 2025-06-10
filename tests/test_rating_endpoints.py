import pytest
import random

# Use fixtures from conftest.py instead of redefining them
@pytest.fixture
def create_category(client, user_auth):
    category_payload = {
        "name": f"Test Category {random.randint(1000, 9999)}",
        "description": "Test Category Description"
    }
    response = client.post("/categories", json=category_payload)
    assert response.status_code == 201, response.text
    return response.json()["id"]

@pytest.fixture
def create_item(client, user_auth, create_category):
    item_payload = {
        "name": f"Item for Rating {random.randint(1000, 9999)}",
        "description": "Item to be rated",
        "category_ids": [create_category],
        "tags": ["tag1"]
    }
    
    response = client.post("/items", json=item_payload, headers=user_auth["headers"])
    assert response.status_code == 201, response.text
    return response.json()["id"]

def test_create_and_get_rating(client, user_auth, create_item):
    # Récupérer l'ID utilisateur via /auth/me
    response = client.get("/auth/me", headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    user_id = response.json()["id"]
    
    rating_payload = {
        "item_id": create_item,
        "user_id": user_id,
        "value": 4,
        "comment": "Very good!"
    }
    response = client.post("/ratings", json=rating_payload, headers=user_auth["headers"])
    assert response.status_code == 201, response.text
    created_rating = response.json()
    assert created_rating["item_id"] == create_item
    assert created_rating["user_id"] == user_id
    assert created_rating["value"] == 4

    rating_id = created_rating["id"]
    response = client.get(f"/ratings/{rating_id}", headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    fetched_rating = response.json()
    assert fetched_rating["id"] == rating_id

def test_list_ratings(client, user_auth):
    # Test listing ratings should fail for normal users (403)
    response = client.get("/ratings", headers=user_auth["headers"])
    assert response.status_code == 403, response.text
    
    # Should work with admin credentials
    admin_auth = client.post("/auth/token", data={"username": "admin@example.com", "password": "adminpassword"})
    if admin_auth.status_code == 200:
        admin_token = admin_auth.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/ratings", headers=admin_headers)
        assert response.status_code == 200, response.text

def test_update_rating(client, user_auth, create_item):
    # Get current user
    response = client.get("/auth/me", headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    user_id = response.json()["id"]
    
    # Create a rating to update
    rating_payload = {
        "item_id": create_item,
        "user_id": user_id,
        "value": 2,
        "comment": "Not so good"
    }
    response = client.post("/ratings", json=rating_payload, headers=user_auth["headers"])
    assert response.status_code == 201, response.text
    rating_id = response.json()["id"]

    # Update the rating
    update_payload = {
        "value": 5,
        "comment": "Actually, it's great!"
    }
    response = client.put(f"/ratings/{rating_id}", json=update_payload, headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    updated_rating = response.json()
    assert updated_rating["value"] == 5
    assert updated_rating["comment"] == "Actually, it's great!"

def test_delete_rating(client, user_auth, create_item):
    # Get the current user's ID
    response = client.get("/auth/me", headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    user_id = response.json()["id"]
    
    # Create a rating with the current user
    rating_payload = {
        "item_id": create_item,
        "user_id": user_id,
        "value": 3,
        "comment": "To be deleted"
    }
    response = client.post("/ratings", json=rating_payload, headers=user_auth["headers"])
    assert response.status_code == 201, response.text
    rating_id = response.json()["id"]

    # Verify the rating was created with the current user
    response = client.get(f"/ratings/{rating_id}", headers=user_auth["headers"])
    assert response.status_code == 200, response.text
    assert response.json()["user_id"] == user_id, "Rating was not created with the expected user ID"

    # Delete the rating
    response = client.delete(f"/ratings/{rating_id}", headers=user_auth["headers"])
    assert response.status_code == 204, response.text

    # Verify the rating was deleted
    response = client.get(f"/ratings/{rating_id}", headers=user_auth["headers"])
    assert response.status_code == 404