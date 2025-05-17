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
    if response.status_code != 201:
        assert response.status_code == 400, response.text

    form_data = {
        "username": create_user_payload["email"],
        "password": create_user_payload["password"]
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def item_id(auth_headers):
    # Crée un item pour pouvoir le noter
    item_payload = {
        "name": "Item for Rating",
        "description": "Item to be rated",
        "category_ids": [1],
        "tags": ["tag1"]
    }
    response = client.post("/items", json=item_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    return response.json()["id"]

def test_create_and_get_rating(auth_headers, item_id):
    # Crée un rating
    rating_payload = {
        "item_id": item_id,
        "value": 4,
        "comment": "Very good!"
    }
    response = client.post("/ratings", json=rating_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    created_rating = response.json()
    assert created_rating["item_id"] == item_id
    assert created_rating["value"] == 4

    # Récupère le rating par ID
    rating_id = created_rating["id"]
    response = client.get(f"/ratings/{rating_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    fetched_rating = response.json()
    assert fetched_rating["id"] == rating_id

def test_list_ratings(auth_headers, item_id):
    # Liste tous les ratings
    response = client.get("/ratings", headers=auth_headers)
    assert response.status_code == 200, response.text
    ratings = response.json()
    assert isinstance(ratings, list)
    assert any(r["item_id"] == item_id for r in ratings)

def test_update_rating(auth_headers, item_id):
    # Crée un rating à mettre à jour
    rating_payload = {
        "item_id": item_id,
        "value": 2,
        "comment": "Not so good"
    }
    response = client.post("/ratings", json=rating_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    rating_id = response.json()["id"]

    # Met à jour le rating
    update_payload = {
        "value": 5,
        "comment": "Actually, it's great!"
    }
    response = client.put(f"/ratings/{rating_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    updated_rating = response.json()
    assert updated_rating["value"] == 5
    assert updated_rating["comment"] == "Actually, it's great!"

def test_delete_rating(auth_headers, item_id):
    # Crée un rating à supprimer
    rating_payload = {
        "item_id": item_id,
        "value": 3,
        "comment": "To be deleted"
    }
    response = client.post("/ratings", json=rating_payload, headers=auth_headers)
    assert response.status_code == 201, response.text
    rating_id = response.json()["id"]

    # Supprime le rating
    response = client.delete(f"/ratings/{rating_id}", headers=auth_headers)
    assert response.status_code == 204, response.text

    # Vérifie qu'il n'existe plus
    response = client.get(f"/ratings/{rating_id}", headers=auth_headers)
    assert response.status_code == 404