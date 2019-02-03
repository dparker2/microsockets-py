import asyncio
import websockets
import json

from .serversocket import ServerSocket


class MicroServer(object):
    handlers = {}

    def __init__(self):
        pass

    def run(self, *, url='localhost', port=8765, key='type'):
        self.url = url
        self.port = port
        self.key = key
        
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.dispatch, self.url, self.port)
        )
        asyncio.get_event_loop().run_forever()

    async def dispatch(self, websocket, path):
        server_socket = ServerSocket(websocket)

        async for message in websocket:
            parsed = json.loads(message)
            name = parsed[self.key]
            response = await self.handlers[name](server_socket, parsed)
            if response:
                await websocket.send(json.dumps({
                    "status": 1,
                    "response": response
                }))

    def register(self, *, key):
        def decorator(handler):
            self.handlers[key] = handler
        return decorator