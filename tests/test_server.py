import pytest
import asyncio
import websockets
from async_generator import yield_, async_generator
from microsockets.server import MicroServer


@pytest.fixture
@async_generator
async def app():
    app = MicroServer()
    await yield_(app)  # yield inside async cannot be used in py3.5
    await app.close()


@pytest.fixture
@async_generator
async def running_app(app):
    await app.run()
    await yield_(app)


@pytest.fixture
async def async_stub(mocker):
    stub = mocker.MagicMock(return_value=asyncio.Future())
    stub.return_value.set_result(('test', 'message'))
    return stub


@pytest.mark.asyncio
async def test_run_defaults(app):
    await app.run()
    async with websockets.connect('ws://localhost:8765') as websocket:
        assert websocket.open


@pytest.mark.asyncio
async def test_run_port(app):
    port = '8000'
    await app.run(port=port)
    async with websockets.connect('ws://localhost:' + port) as websocket:
        assert websocket.open


@pytest.mark.asyncio
async def test_handler_exists(running_app, async_stub):
    running_app.register(key='TestKey')(async_stub)

    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send('{"type":"TestKey"}')

    assert async_stub.call_count == 1


@pytest.mark.asyncio
async def test_handler_not_exists(running_app, async_stub):
    running_app.register(key='TestKey')(async_stub)

    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send('{"type":"WrongKey"}')

    assert async_stub.call_count == 0


@pytest.mark.asyncio
async def test_register_handlers(app, async_stub):
    class MockHandlers(object):
        pass

    mockHandlers = MockHandlers()
    mockHandlers.handlers = {'TestKey':async_stub}

    app.register_handlers(mockHandlers)
    await app.run()

    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send('{"type":"TestKey"}')

    assert async_stub.call_count == 1
