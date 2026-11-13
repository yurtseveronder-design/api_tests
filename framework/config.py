"""Central configuration. Everything can be overridden with environment variables."""

import os

DEFAULT_TIMEOUT = float(os.getenv("API_TESTS_TIMEOUT", "10"))
USER_AGENT = "api-tests/2.0"

# Public demo API used for the contract / CRUD examples.
JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"

# Named targets for the --env option. staging/prod are read from the environment
# so no placeholder hostnames live in the repository.
ENVIRONMENTS = {
    "dev": lambda: JSONPLACEHOLDER_URL,
    "staging": lambda: os.getenv("STAGING_BASE_URL"),
    "prod": lambda: os.getenv("PROD_BASE_URL"),
}

# ai-sentinel gateway (https://github.com/yurtseveronder-design/ai-sentinel)
SENTINEL_BASE_URL = os.getenv("SENTINEL_BASE_URL", "http://127.0.0.1:8000")
SENTINEL_API_KEY = os.getenv("SENTINEL_API_KEY", "test-api-key")
# Set to "1" (CI does) to fail instead of skip when the gateway is unreachable.
SENTINEL_REQUIRED = os.getenv("SENTINEL_REQUIRED", "0") == "1"


def resolve_base_url(env: str) -> str:
    """Return the base URL for a named environment or raise a clear error."""
    try:
        getter = ENVIRONMENTS[env.lower()]
    except KeyError:
        raise ValueError(f"Unknown environment '{env}'. Choose one of: {', '.join(ENVIRONMENTS)}")
    url = getter()
    if not url:
        var = {"staging": "STAGING_BASE_URL", "prod": "PROD_BASE_URL"}.get(env.lower(), "the base URL")
        raise ValueError(f"Environment '{env}' is not configured. Set {var}.")
    return url.rstrip("/")
