import pytest
from config import BASE_URL
from utils.api_client import APIClient


@pytest.fixture
def api_client():
    return APIClient(BASE_URL)


@pytest.fixture
def sample_user_payload():
    return {
        "name": "Alex TechOps",
        "username": "alex_qa",
        "email": "alex@example.com",
    }