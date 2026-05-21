import pytest
import respx
import httpx

from ravelpy import RavelryClient

BASE = "https://api.ravelry.com"


@pytest.fixture
def client():
    return RavelryClient(username="testuser", api_key="testkey")


@pytest.fixture
def mock_api():
    with respx.mock(base_url=BASE, assert_all_called=False) as mock:
        yield mock
