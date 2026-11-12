import pytest
from client import APIClient

ENV_URLS = {
    "dev": "https://jsonplaceholder.typicode.com",
    "auth_test": "https://httpbin.org",
    "staging": "https://staging.api.example.com",
    "prod": "https://api.example.com"
}

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="dev", help="Target environment: dev, staging, or prod"
    )

@pytest.fixture(scope="session")
def base_url(request):
    """Resolve base URL from command line --env option."""
    env = request.config.getoption("--env").lower()
    return ENV_URLS.get(env, ENV_URLS["dev"])

@pytest.fixture(scope="session")
def api_client(base_url):
    """Default API client fixture."""
    return APIClient(base_url=base_url)

@pytest.fixture
def bearer_client(base_url):
    """Client configured with a Bearer Token."""
    token = "test-bearer-token-12345"
    return APIClient(base_url=base_url, auth_type="bearer", credentials=token)

@pytest.fixture
def api_key_client(base_url):
    """Client configured with an API Key Header."""
    key = "secret-api-key-abcde"
    return APIClient(base_url=base_url, auth_type="api_key", credentials=key, api_key_header="X-API-Key")

@pytest.fixture
def basic_auth_client(base_url):
    """Client configured with Basic Auth."""
    return APIClient(base_url=base_url, auth_type="basic", credentials=("testuser", "testpassword"))

@pytest.fixture
def sample_user_payload():
    return {
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz"
    }