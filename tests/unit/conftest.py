import pytest

from framework.client import APIClient
from tests.unit.stub_server import StubServer


@pytest.fixture
def stub():
    server = StubServer().start()
    yield server
    server.stop()


@pytest.fixture
def client(stub):
    """Client with instant backoff so retry tests stay fast."""
    with APIClient(stub.url, retries=2, backoff_factor=0, timeout=2) as c:
        yield c
