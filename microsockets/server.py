import asyncio
import websockets
import json

from .serversocket import ServerSocket
from .servermessageprocessor import MessageProcessor
from .router import Router


class MicroServer(object):
    def __init__(self):
        self.router = Router()
        self.server = None
        self.url = None
        self.port = None

    def run(self, *, 
        url='localhost', 
        port=8765, 
        key='type', 
        MsgProcessorClass=MessageProcessor
    ):
        self.url = url
        self.port = port
        self.router.set_msg_processor(MsgProcessorClass(key))

        loop = asyncio.get_event_loop()
        # If a loop is already running (eg during tests) return an awaitable
        if loop.is_running():
            return asyncio.ensure_future(self.__run())
        else:
            asyncio.get_event_loop().run_until_complete(self.__run())
            asyncio.get_event_loop().run_forever()


    async def __run(self):
        self.server = await websockets.serve(self.router.dispatch, self.url, self.port)


    async def close(self):
        self.server.close()
        await self.server.wait_closed()


    def register(self, *, key):
        def decorator(handler):
            self.router.set_handler(key, handler)
        return decorator


    def register_handlers(self, handlers):
        for key, handler in handlers.handlers.items():
            self.register(key=key)(handler)
