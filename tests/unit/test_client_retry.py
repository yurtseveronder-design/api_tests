import pytest
import requests

from framework.client import APIClient


def test_get_retries_transient_503_then_succeeds(stub, client):
    stub.enqueue(503).enqueue(503).enqueue(200, {"ok": True})
    assert client.get("/x").status_code == 200
    assert len(stub.requests) == 3


def test_get_returns_final_5xx_after_retries_exhausted(stub, client):
    for _ in range(5):
        stub.enqueue(503)
    assert client.get("/x").status_code == 503
    assert len(stub.requests) == 3  # 1 attempt + 2 retries


def test_post_is_not_retried(stub, client):
    stub.enqueue(503).enqueue(200)
    assert client.post("/x", json={"a": 1}).status_code == 503
    assert len(stub.requests) == 1


@pytest.mark.parametrize("status", [400, 401, 404, 422])
def test_client_errors_are_not_retried(stub, client, status):
    stub.enqueue(status)
    assert client.get("/x").status_code == status
    assert len(stub.requests) == 1


def test_timeout_raises(stub):
    stub.enqueue(200, delay=1.0)
    with APIClient(stub.url, retries=0, timeout=0.2) as c:
        with pytest.raises(requests.exceptions.ReadTimeout):
            c.get("/slow")


def test_connection_error_is_raised_after_retries():
    with APIClient("http://127.0.0.1:9", retries=1, backoff_factor=0, timeout=1) as c:
        with pytest.raises(requests.exceptions.ConnectionError):
            c.get("/")
