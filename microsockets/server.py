import asyncio
import websockets
import json

from .serversocket import ServerSocket
from .servermessageprocessor import MessageProcessor


class MicroServer(object):
    def __init__(self):
        self.handlers = {}
        self.server = None  # Set by __run

    def run(self, *, 
        url='localhost', 
        port=8765, 
        key='type', 
        MsgProcessorClass=MessageProcessor
    ):
        self.url = url
        self.port = port
        self.msg_processor = MsgProcessorClass(key)

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
            # equiv to async for message in websocket
            while True:
                message = await websocket.recv()
                key, argument = self.msg_processor.extract_handler_arguments(message)
                response = await self.handlers[key](server_socket, *argument if isinstance(argument, list) else argument)

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
