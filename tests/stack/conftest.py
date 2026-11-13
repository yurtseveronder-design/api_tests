"""End-to-end fixtures: sentinel-ui -> ai-sentinel -> sentinel-semantic must all be running."""

import pytest
import requests

from framework import config
from framework.client import APIClient

SERVICES = {
    "sentinel-ui": config.UI_BASE_URL,
    "ai-sentinel": config.SENTINEL_BASE_URL,
    "sentinel-semantic": config.SEMANTIC_BASE_URL,
}


@pytest.fixture(scope="session", autouse=True)
def full_stack():
    for name, url in SERVICES.items():
        try:
            requests.get(f"{url}/health", timeout=3).raise_for_status()
        except requests.RequestException as exc:
            message = f"{name} not reachable at {url}: {exc}"
            if config.SENTINEL_REQUIRED:
                pytest.fail(message, pytrace=False)
            pytest.skip(message)


@pytest.fixture(scope="session")
def ui():
    with APIClient(config.UI_BASE_URL, auth_type="api_key", credentials=config.UI_API_KEY) as c:
        yield c


@pytest.fixture(scope="session")
def ui_anon():
    with APIClient(config.UI_BASE_URL) as c:
        yield c


@pytest.fixture(scope="session")
def gateway():
    with APIClient(config.SENTINEL_BASE_URL, auth_type="api_key", credentials=config.SENTINEL_API_KEY) as c:
        yield c
