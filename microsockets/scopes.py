import json
from abc import ABC
from . import socket
from . import middleware


class Scope(ABC):
    async def __call__(self, scope, receive, send):
        pass


class LifespanScope(Scope):
    async def __call__(self, scope, receive, send):
        print("lifespan called")
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                print("startup")
                # on_startup()
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                print("shutdown")
                # on_shutdown()
                await send({"type": "lifespan.shutdown.complete"})
                return


class WebsocketScope(Scope):
    def __init__(self, router):
        self.middleware = middleware.Middleware()
        self.__router = router

    async def __call__(self, scope, receive, send):
        ws = socket.Socket(scope, send)
        while True:
            message = await receive()
            print(message)
            if message["type"] == "websocket.connect":
                # Hook here to control acceptance?
                await send({"type": "websocket.accept"})
            elif message["type"] == "websocket.receive":
                # Hook here to control receive?
                try:
                    loaded = json.loads(message["text"])
                    event = loaded["event"]
                    payload = loaded["payload"]
                except (json.JSONDecodeError, KeyError):
                    continue  # wrong format, ignore for now. maybe expose an error handler?
                else:
                    handler = self.__router(event)
                    if handler:
                        ws.payload = payload
                        ws.event = event
                        if len(self.middleware.before_on) > 0:
                            await self.middleware.before_on[0](ws, handler)
                        else:
                            await handler(ws)
                        # after_on()
            elif message["type"] == "websocket.disconnect":
                # after_disconnect()
                return

    def add_event(self, event, func):
        self.__router.add(event, func)
