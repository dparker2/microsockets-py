import pytest
from .serverhandlers import Handlers


@pytest.fixture
def handlers():
    return Handlers()


def test_register(handlers):
    def handler():
        pass
    handlers.register(key='TestKey')(handler)
    assert handlers.handlers['TestKey'] == handler