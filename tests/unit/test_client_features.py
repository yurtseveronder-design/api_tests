import base64

import pytest

from framework import config
from framework.client import APIClient, APIResponseError


def sent_headers(stub):
    return {k.lower(): v for k, v in stub.requests[-1]["headers"].items()}


def test_url_joining_handles_slashes(stub):
    with APIClient(stub.url + "/", retries=0) as c:
        c.get("users")
        c.get("/users")
    assert [r["path"] for r in stub.requests] == ["/users", "/users"]


def test_bearer_auth(stub):
    with APIClient(stub.url, auth_type="bearer", credentials="tok", retries=0) as c:
        c.get("/")
    assert sent_headers(stub)["authorization"] == "Bearer tok"


def test_basic_auth_tuple_is_base64_encoded(stub):
    with APIClient(stub.url, auth_type="basic", credentials=("user", "pass"), retries=0) as c:
        c.get("/")
    token = sent_headers(stub)["authorization"].removeprefix("Basic ")
    assert base64.b64decode(token).decode() == "user:pass"


def test_api_key_uses_custom_header(stub):
    with APIClient(stub.url, auth_type="api_key", credentials="k", api_key_header="X-Token", retries=0) as c:
        c.get("/")
    assert sent_headers(stub)["x-token"] == "k"


def test_clear_auth_removes_headers(stub):
    with APIClient(stub.url, auth_type="bearer", credentials="tok", retries=0) as c:
        c.clear_auth()
        c.get("/")
    assert "authorization" not in sent_headers(stub)


def test_unsupported_auth_type_raises():
    with pytest.raises(ValueError):
        APIClient("http://x", auth_type="magic", credentials="y")


def test_per_request_header_override(stub):
    with APIClient(stub.url, auth_type="bearer", credentials="tok", retries=0) as c:
        c.get("/", headers={"Authorization": "Bearer other"})
    assert sent_headers(stub)["authorization"] == "Bearer other"


def test_default_user_agent_is_sent(stub, client):
    client.get("/")
    assert sent_headers(stub)["user-agent"] == config.USER_AGENT


def test_expect_status_mismatch_raises_readable_error(stub, client):
    stub.enqueue(404, {"detail": "nope"})
    with pytest.raises(APIResponseError) as exc:
        client.get("/missing", expect_status=200)
    assert exc.value.status_code == 404
    assert "expected 200, got 404" in str(exc.value)


def test_expect_status_match_passes(stub, client):
    stub.enqueue(201, {"id": 1})
    assert client.post("/x", expect_status=201, json={}).json() == {"id": 1}


def test_raise_on_error(stub, client):
    stub.enqueue(400)
    with pytest.raises(APIResponseError):
        client.get("/", raise_on_error=True)


def test_json_body_round_trip(stub, client):
    client.put("/x", json={"a": 1})
    assert stub.requests[-1]["method"] == "PUT"
    assert stub.requests[-1]["body"] == b'{"a": 1}'
    client.delete("/x")
    assert stub.requests[-1]["method"] == "DELETE"


def test_resolve_base_url(monkeypatch):
    assert config.resolve_base_url("dev") == config.JSONPLACEHOLDER_URL
    monkeypatch.delenv("STAGING_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="STAGING_BASE_URL"):
        config.resolve_base_url("staging")
    monkeypatch.setenv("STAGING_BASE_URL", "https://stg.example.test/")
    assert config.resolve_base_url("staging") == "https://stg.example.test"
    with pytest.raises(ValueError, match="Unknown"):
        config.resolve_base_url("nope")
