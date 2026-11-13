import pytest

from schemas import UserSchema


def test_list_users_matches_contract(api_client):
    response = api_client.get("/users", expect_status=200)
    users = response.json()
    assert len(users) == 10
    for user in users:
        UserSchema(**user)


def test_get_single_user(api_client):
    user = UserSchema(**api_client.get("/users/1", expect_status=200).json())
    assert user.id == 1
    assert user.address.geo.lat


@pytest.mark.parametrize("user_id", [0, 999999])
def test_unknown_user_returns_404(api_client, user_id):
    assert api_client.get(f"/users/{user_id}").status_code == 404
