import pytest
import asyncio
import websockets
from async_generator import yield_, async_generator
from .serversocket import ServerSocket


@pytest.fixture
def MockWebsocket():
    class MockSocket(object):
        async def send(self, arg):
            print('hmm')
    return MockSocket


@pytest.mark.asyncio
async def test_pub_others(MockWebsocket, mocker):
    # Spy internal websocket.send and subscribe to a topic
    mock_websocket = MockWebsocket()
    spy = mocker.spy(mock_websocket, 'send')
    othersocket = ServerSocket(mock_websocket)
    othersocket.subscribe('Test')

    # Publish to the topic
    mainsocket = ServerSocket(MockWebsocket())
    mainsocket.subscribe('Test')
    mainsocket.publish_to_others('Test', 'Test')
    await asyncio.sleep(0)  # Let other tasks run (the websocket.send)
    assert spy.call_count == 1


def test_unsubscribe(MockWebsocket):
    socket = ServerSocket(MockWebsocket())
    socket.subscribe('Test')
    socket.unsubscribe('Test')
    socket.unsubscribe('Test')  # Should not raise KeyError

    socket.subscribe('Test')
    socket.unsubscribe_all()
    socket.unsubscribe_all()  # Should not raise KeyError