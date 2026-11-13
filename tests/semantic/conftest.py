"""Fixtures for the sentinel-semantic tests (service must be running; see README)."""

import pytest
import requests

from framework import config
from framework.client import APIClient


@pytest.fixture(scope="session")
def semantic_url():
    try:
        requests.get(f"{config.SEMANTIC_BASE_URL}/health", timeout=3).raise_for_status()
    except requests.RequestException as exc:
        message = f"sentinel-semantic not reachable at {config.SEMANTIC_BASE_URL}: {exc}"
        if config.SENTINEL_REQUIRED:
            pytest.fail(message, pytrace=False)
        pytest.skip(message)
    return config.SEMANTIC_BASE_URL


@pytest.fixture(scope="session")
def semantic(semantic_url):
    with APIClient(semantic_url, auth_type="api_key", credentials=config.SEMANTIC_API_KEY) as c:
        yield c


@pytest.fixture(scope="session")
def semantic_anon(semantic_url):
    with APIClient(semantic_url) as c:
        yield c
