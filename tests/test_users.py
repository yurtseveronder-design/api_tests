import pytest

# --- READ TESTS ---


def test_get_users_status_code_and_schema(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0

    first_user = users[0]
    assert isinstance(first_user["id"], int)
    assert isinstance(first_user["name"], str)
    assert isinstance(first_user["username"], str)
    assert isinstance(first_user["email"], str)
    assert "@" in first_user["email"]


# --- CREATE TESTS ---


def test_create_user_response_data(api_client, sample_user_payload):
    response = api_client.post("/users", sample_user_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_user_payload["name"]
    assert data["email"] == sample_user_payload["email"]
    assert isinstance(data["id"], int)


# --- UPDATE TESTS (PUT) ---


def test_update_user_returns_updated_data(api_client):
    updated_payload = {
        "name": "Alex Updated",
        "username": "alex_qa_updated",
        "email": "alex_updated@example.com",
    }
    response = api_client.put("/users/1", updated_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == updated_payload["name"]
    assert data["email"] == updated_payload["email"]


# --- DELETE TESTS ---


def test_delete_user_returns_200(api_client):
    response = api_client.delete("/users/1")
    assert response.status_code == 200


# --- NEGATIVE TESTS (PARAMETRIZED) ---


@pytest.mark.parametrize(
    "invalid_path",
    [
        "/users/999999",
        "/invalid_endpoint",
        "/posts/0000",
    ],
)
def test_invalid_endpoints_return_404(api_client, invalid_path):
    response = api_client.get(invalid_path)
    assert response.status_code == 404