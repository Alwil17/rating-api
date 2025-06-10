import pytest
import random
from fastapi.testclient import TestClient
from app.api.main import app

@pytest.fixture
def category_id(client):
    category_payload = {
        "name": f"Test Category {random.randint(1000, 9999)}",
        "description": "Test Category Description"
    }
    response = client.post("/categories", json=category_payload)
    assert response.status_code == 201, response.text
    return response.json()["id"]

def auth_headers(client):
    # Crée un utilisateur et récupère un token d'authentification
    create_user_payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=create_user_payload)
    if response.status_code != 201:  # Si l'utilisateur existe déjà
        assert response.status_code == 400, response.text

    form_data = {
        "username": create_user_payload["email"],
        "password": create_user_payload["password"]
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_get_item(client, user_auth, category_id):
    item_payload = {
        "name": f"Test Item {random.randint(1000, 9999)}",
        "description": "This is a test item",
        "category_ids": [category_id],
        "tags": ["test", "sample"]
    }
    
    # Create an item
    response = client.post("/items", json=item_payload, headers=user_auth["headers"])
    assert response.status_code == 201, response.text
    item = response.json()
    assert item["name"] == item_payload["name"]
    assert item["description"] == item_payload["description"]
    
    # Get the item by ID
    item_id = item["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    fetched_item = response.json()
    assert fetched_item["id"] == item_id
    assert fetched_item["name"] == item_payload["name"]

def test_list_items_with_filters(client, admin_auth, category_id):
    # Create a few items
    for i in range(3):
        item_payload = {
            "name": f"Filtered Item {i}",
            "description": f"Filtered item description {i}",
            "category_ids": [category_id],
            "tags": ["filter", f"tag{i}"]
        }
        response = client.post("/items", json=item_payload, headers=admin_auth["headers"])
        assert response.status_code == 201, response.text
    
    # Test filters
    
    # By category
    response = client.get(f"/items?category_id={category_id}")
    assert response.status_code == 200, response.text
    items = response.json()
    assert len(items) > 0
    
    # By tag
    response = client.get("/items?tags=filter")
    assert response.status_code == 200, response.text
    items = response.json()
    assert len(items) > 0

def test_update_item(client, admin_auth, category_id):
    # Create an item to update
    item_payload = {
        "name": "Item to Update",
        "description": "This will be updated",
        "image_url": "http://example.com/image.jpg",
        "category_ids": [category_id],
        "tags": ["update"]
    }
    response = client.post("/items", json=item_payload, headers=admin_auth["headers"])
    assert response.status_code == 201, response.text
    item_id = response.json()["id"]
    
    # Update the item
    update_payload = {
        "name": "Updated Item Name",
        "description": "Updated description",
        "image_url": "http://example.com/image.jpg",
        "category_ids": [category_id],
        "tags": ["updated"]
    }
    response = client.put(f"/items/{item_id}", json=update_payload, headers=admin_auth["headers"])
    assert response.status_code == 200, response.text
    updated_item = response.json()
    assert updated_item["name"] == update_payload["name"]
    assert updated_item["description"] == update_payload["description"]

def test_delete_item(client, admin_auth, category_id):
    # Create an item to delete
    item_payload = {
        "name": "Item to Delete",
        "description": "This will be deleted",
        "category_ids": [category_id],
        "tags": ["delete"]
    }
    response = client.post("/items", json=item_payload, headers=admin_auth["headers"])
    assert response.status_code == 201, response.text
    item_id = response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/items/{item_id}", headers=admin_auth["headers"])
    assert response.status_code == 204, response.text
    
    # Verify it was deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 400