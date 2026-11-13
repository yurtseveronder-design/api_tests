import pytest


@pytest.mark.parametrize("endpoint", [
    "/users/999999",
    "/posts/999999",
    "/comments/999999",
    "/invalid_endpoint",
])
def test_missing_resources_return_404(api_client, endpoint):
    assert api_client.get(endpoint).status_code == 404
