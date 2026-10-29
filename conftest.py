import pytest
from utils.api_client import APIClient

ENV_URLS = {
    "dev": "https://jsonplaceholder.typicode.com",
    "staging": "https://jsonplaceholder.typicode.com",
    "prod": "https://jsonplaceholder.typicode.com"
}

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment: dev, staging, or prod"
    )

@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env").lower()
    return ENV_URLS.get(env, ENV_URLS["dev"])

@pytest.fixture(scope="session")
def api_client(base_url):
    return APIClient(base_url=base_url)

@pytest.fixture
def sample_user_payload():
    return {
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz"
    }