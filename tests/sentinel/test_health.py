from schemas import HealthSchema


def test_health_contract(sentinel_anon):
    response = sentinel_anon.get("/health", expect_status=200)
    assert HealthSchema(**response.json()).status == "ok"


def test_security_headers_present(sentinel_anon):
    headers = sentinel_anon.get("/health").headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["Content-Security-Policy"] == "default-src 'none'"


def test_request_id_generated_and_echoed(sentinel_anon):
    generated = sentinel_anon.get("/health").headers["X-Request-ID"]
    assert generated
    echoed = sentinel_anon.get("/health", headers={"X-Request-ID": "trace-123"}).headers["X-Request-ID"]
    assert echoed == "trace-123"
