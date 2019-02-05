import asyncio
import websockets
import json

from .serversocket import ServerSocket


class MicroServer(object):
    def __init__(self):
        self.handlers = {}
        self.server = None  # Set by __run

    def run(self, *, url='localhost', port=8765, key='type'):
        self.url = url
        self.port = port
        self.key = key

        loop = asyncio.get_event_loop()
        # If a loop is already running (eg during tests) return an awaitable
        if loop.is_running():
            return asyncio.ensure_future(self.__run())
        else:
            asyncio.get_event_loop().run_until_complete(self.__run())
            asyncio.get_event_loop().run_forever()


    async def __run(self):
        self.server = await websockets.serve(self.dispatch, self.url, self.port)


    async def dispatch(self, websocket, path):
        server_socket = ServerSocket(websocket)

        try: 
            while True:
                message = await websocket.recv()
                parsed = json.loads(message)
                name = parsed[self.key]
                response = await self.handlers[name](server_socket, parsed)
                if response:
                    await websocket.send(json.dumps({
                        "status": 1,
                        "response": response
                    }))
        except websockets.exceptions.ConnectionClosed:
            server_socket.unsubscribe_all()


    async def close(self):
        self.server.close()
        await self.server.wait_closed()


    def register(self, *, key):
        def decorator(handler):
            self.handlers[key] = handler
        return decorator


    def register_handlers(self, handlers):
        for key, handler in handlers.handlers.items():
            self.register(key=key)(handler)
