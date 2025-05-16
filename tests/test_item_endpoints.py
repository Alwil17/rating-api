import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def auth_headers():
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

def test_create_and_get_item(auth_headers):
    # Test de création d'un item
    item_payload = {
        "name": "Test Item",
        "description": "This is a test item",
        "image_url": "",
        "category_ids": [1],
        "tags": ["tag1", "tag2"]
    }
    response = client.post("/items", json=item_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    created_item = response.json()
    assert created_item["name"] == item_payload["name"]
    assert created_item["description"] == item_payload["description"]

    # Test de récupération de l'item créé
    item_id = created_item["id"]
    response = client.get(f"/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    fetched_item = response.json()
    assert fetched_item["name"] == item_payload["name"]
    assert fetched_item["description"] == item_payload["description"]

def test_list_items_with_filters(auth_headers):
    # Création de plusieurs items
    item_payload_1 = {
        "name": "Item 1",
        "description": "Description for Item 1",
        "category_ids": [1],
        "tags": ["tag1", "tag2"]
    }
    item_payload_2 = {
        "name": "Item 2",
        "description": "Description for Item 2",
        "category_ids": [2],
        "tags": ["tag2", "tag3"]
    }

    client.post("/items", json=item_payload_1, headers=auth_headers)
    client.post("/items", json=item_payload_2, headers=auth_headers)

    # Test de liste sans filtres
    response = client.get("/items", headers=auth_headers)
    assert response.status_code == 200, response.text
    items = response.json()
    assert len(items) >= 2

    # Test de liste avec filtre par catégorie
    response = client.get("/items?category_id=1", headers=auth_headers)
    assert response.status_code == 200, response.text
    filtered_items = response.json()
    assert all(1 in [cat["id"] for cat in item["categories"]] for item in filtered_items)

    # Test de liste avec filtre par tags
    response = client.get("/items?tags=tag2", headers=auth_headers)
    assert response.status_code == 200, response.text
    filtered_items = response.json()
    assert any("tag2" in [tag["name"] for tag in item["tags"]] for item in filtered_items)

def test_update_item(auth_headers):
    # Création d'un item
    item_payload = {
        "name": "Item to Update",
        "description": "Original description",
        "category_ids": [1],
        "tags": ["tag1"]
    }
    response = client.post("/items", json=item_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    created_item = response.json()

    # Mise à jour de l'item
    update_payload = {
        "name": "Updated Item",
        "description": "Updated description",
        "category_ids": [2],
        "tags": ["tag2", "tag3"]
    }
    item_id = created_item["id"]
    response = client.put(f"/items/{item_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 403, response.text

def test_delete_item(auth_headers):
    # Création d'un item
    item_payload = {
        "name": "Item to Delete",
        "description": "This item will be deleted",
        "category_ids": [1],
        "tags": ["tag1"]
    }
    response = client.post("/items", json=item_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    created_item = response.json()

    # Suppression de l'item 
    item_id = created_item["id"]
    response = client.delete(f"/items/{item_id}", headers=auth_headers)
    assert response.status_code == 403, response.text