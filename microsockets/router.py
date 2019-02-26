import websockets
import json

from .serversocket import ServerSocket


class Router(object):
    def __init__(self):
        self.handlers = {}
        self.unmarshaller = None


    async def handle_connection(self, websocket, path):
        server_socket = ServerSocket(websocket)

        try:
            await self.__dispatch_forever(server_socket, path)
        except websockets.exceptions.ConnectionClosed:
            server_socket.unsubscribe_all()


    async def __dispatch_forever(self, server_socket, path):
        # equiv to async for message in websocket
        while True:
            message = await server_socket.recv()
            key, argument = self.unmarshaller.get_handler_arguments(message)
            response = await self.handlers[key](server_socket, *argument if isinstance(argument, list) else argument)

            if response:
                await server_socket.send(json.dumps({
                    "status": 1,
                    "response": response
                }))


    def set_handler(self, key, handler):
        self.handlers[key] = handler


    def set_unmarshaller(self, unmarshaller):
        self.unmarshaller = unmarshaller
