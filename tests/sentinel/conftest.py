"""Fixtures for the ai-sentinel gateway tests.

Start the gateway first, e.g.:
    AI_SENTINEL_API_KEY=test-api-key uvicorn ai_sentinel.api.gateway:app
Without a reachable gateway these tests are skipped (or fail when SENTINEL_REQUIRED=1).
"""

import pytest
import requests

from framework import config
from framework.client import APIClient


@pytest.fixture(scope="session")
def sentinel_url():
    try:
        requests.get(f"{config.SENTINEL_BASE_URL}/health", timeout=3).raise_for_status()
    except requests.RequestException as exc:
        message = f"ai-sentinel gateway not reachable at {config.SENTINEL_BASE_URL}: {exc}"
        if config.SENTINEL_REQUIRED:
            pytest.fail(message, pytrace=False)
        pytest.skip(message)
    return config.SENTINEL_BASE_URL


@pytest.fixture(scope="session")
def sentinel(sentinel_url):
    """Authenticated client."""
    with APIClient(sentinel_url, auth_type="api_key", credentials=config.SENTINEL_API_KEY) as c:
        yield c


@pytest.fixture(scope="session")
def sentinel_anon(sentinel_url):
    """Client without credentials."""
    with APIClient(sentinel_url) as c:
        yield c
