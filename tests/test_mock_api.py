import pytest
from client import APIClient

def test_mock_server_error_handling(httpserver):
    # Setup mock server response for a custom endpoint
    httpserver.expect_request("/flaky-endpoint").respond_with_json(
        {"error": "Service Unavailable"}, status=503
    )

    # Point client to local mock server URL
    client = APIClient(base_url=httpserver.url_for(""))
    response = client.get("/flaky-endpoint")

    # Assert client correctly captures the mock status
    assert response.status_code == 503
    assert response.json()["error"] == "Service Unavailable"