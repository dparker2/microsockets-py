import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"type":"NewMessage", "body":"Message body!"}')
        resp = await websocket.recv()
        print(resp)

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:8765'))
