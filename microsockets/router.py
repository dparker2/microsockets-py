import websockets
import json

from .serversocket import ServerSocket


class Router(object):
    def __init__(self):
        self.handlers = {}
        self.marshaller = None
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
            key, argument = self.unmarshaller.extract_handler_arguments(message)
            arguments = argument if isinstance(argument, list) else [argument]
            response = await self.handlers[key](server_socket, *arguments)

            if response:
                ws_resp = self.marshaller.to_string(response[0], response[1])
                await server_socket.send(ws_resp)


    def set_handler(self, key, handler):
        self.handlers[key] = handler


    def set_marshallers(self, marshaller, unmarshaller):
        self.marshaller = marshaller
        self.unmarshaller = unmarshaller