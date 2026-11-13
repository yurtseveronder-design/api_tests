import pytest

from framework import config
from framework.client import APIClient

_DIR_MARKERS = {"unit": "unit", "jsonplaceholder": "external", "sentinel": "sentinel",
                "semantic": "semantic", "stack": "stack"}


def pytest_addoption(parser):
    parser.addoption("--env", default="dev", choices=list(config.ENVIRONMENTS),
                     help="Target environment for the main API tests (default: dev)")
    parser.addoption("--base-url", default=None,
                     help="Override the base URL of the main API tests")


def pytest_collection_modifyitems(items):
    """Mark tests by folder so `-m unit`, `-m external`, `-m sentinel` just work."""
    for item in items:
        if item.get_closest_marker("rate_limit"):
            continue  # keep the destructive test out of `-m sentinel`
        for folder, marker in _DIR_MARKERS.items():
            if f"/tests/{folder}/" in str(item.fspath).replace("\\", "/"):
                item.add_marker(getattr(pytest.mark, marker))


@pytest.fixture(scope="session")
def base_url(request):
    override = request.config.getoption("--base-url")
    if override:
        return override.rstrip("/")
    try:
        return config.resolve_base_url(request.config.getoption("--env"))
    except ValueError as exc:
        pytest.exit(str(exc), returncode=4)


@pytest.fixture(scope="session")
def api_client(base_url):
    with APIClient(base_url=base_url) as client:
        yield client


@pytest.fixture
def post_payload():
    return {"title": "api-tests", "body": "created by the test suite", "userId": 1}
