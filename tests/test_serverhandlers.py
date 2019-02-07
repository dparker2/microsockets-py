import pytest
from microsockets.serverhandlers import Handlers


@pytest.fixture
def handlers():
    return Handlers()


def test_register(handlers, mocker):
    stub = mocker.stub()
    handlers.register(key='TestKey')(stub)
    assert handlers.handlers['TestKey'] == stub