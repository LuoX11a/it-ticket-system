import pytest

from tickets.storage import InMemoryStore


@pytest.fixture
def store():
    return InMemoryStore()
