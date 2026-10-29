import pytest
from schemas.user_schema import UserSchema

def test_get_users_status_code_and_schema(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0

    # Validate the full data contract structure of the first returned user
    validated_user = UserSchema(**users[0])
    assert validated_user.id == users[0]["id"]

def test_create_user_response_data(api_client, sample_user_payload):
    response = api_client.post("/users", json=sample_user_payload)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == sample_user_payload["name"]
    assert created_user["email"] == sample_user_payload["email"]

def test_update_user_returns_updated_data(api_client):
    payload = {"name": "Updated Name"}
    response = api_client.put("/users/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_user_returns_200(api_client):
    response = api_client.delete("/users/1")
    assert response.status_code == 200