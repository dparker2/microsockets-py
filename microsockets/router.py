import websockets
import json

from .serversocket import ServerSocket


class Router(object):
    def __init__(self):
        self.handlers = {}
        self.msg_processor = None


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

    
    def set_handler(self, key, handler):
        self.handlers[key] = handler


    def set_msg_processor(self, processor):
        self.msg_processor = processor