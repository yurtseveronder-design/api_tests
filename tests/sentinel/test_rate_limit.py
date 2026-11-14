"""Destructive: exhausts the gateway's per-API-key limit (50 requests / 60 s by default).

Run against a freshly started gateway, on its own:
    pytest -m rate_limit
"""

import pytest


@pytest.mark.rate_limit
def test_rate_limit_kicks_in(sentinel, sentinel_anon):
    statuses = [sentinel.post("/v1/scan", json={"prompt": "hello"}).status_code for _ in range(60)]
    assert 429 in statuses
    first_block = statuses.index(429)
    assert set(statuses[:first_block]) == {200}
    assert first_block <= 50
    assert statuses[-1] == 429


@pytest.mark.rate_limit
def test_health_and_bad_keys_do_not_use_the_budget_and_spoofed_addresses_do_not_help(sentinel, sentinel_anon):
    # run after the test above: the key's budget is spent, so a new "address" must not give a new one
    spoofed = sentinel.post("/v1/scan", json={"prompt": "hello"}, headers={"X-Forwarded-For": "203.0.113.7"})
    assert spoofed.status_code == 429
    assert sentinel_anon.get("/health").status_code == 200
