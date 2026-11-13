"""Destructive: exhausts the gateway's per-IP limit (50 requests / 60 s).

Run against a freshly started gateway, on its own:
    pytest -m rate_limit
"""

import pytest


@pytest.mark.rate_limit
def test_rate_limit_kicks_in(sentinel_anon):
    statuses = [sentinel_anon.get("/health").status_code for _ in range(60)]
    assert 429 in statuses
    first_block = statuses.index(429)
    assert set(statuses[:first_block]) == {200}
    assert first_block <= 50
    assert statuses[-1] == 429
