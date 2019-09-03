import json
from abc import ABC
from . import socket
from . import rooms


class Scope(ABC):
    def __init__(self, *, hooks, **kwargs):
        self.hooks = hooks

    async def __call__(self, scope, receive, send):
        pass


class LifespanScope(Scope):
    async def __call__(self, scope, receive, send):
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                for hook in self.hooks.on_startup:
                    await hook()  # pass in app?
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                for hook in self.hooks.on_shutdown:
                    await hook()  # pass in app?
                await send({"type": "lifespan.shutdown.complete"})
                return


class WebsocketScope(Scope):
    def __init__(self, *, event_router, room_manager, **kwargs):
        super().__init__(**kwargs)
        self.event_router = event_router
        self.room_manager = room_manager

    async def __call__(self, scope, receive, send):
        ws = socket.Socket(scope, send, self.room_manager)
        while True:
            ws.code = None
            message = await receive()
            if message["type"] == "websocket.connect":
                hook_result = await self.connect_hook(ws)
                try:
                    # Will throw if hooks returned None, so close connection
                    headers, subprotocol = hook_result
                except TypeError:
                    await ws.close()
                else:
                    await send(
                        dict(
                            type="websocket.accept",
                            headers=headers,
                            subprotocol=subprotocol,
                        )
                    )
                    ws.connected = True
            elif message["type"] == "websocket.receive":
                try:
                    loaded = json.loads(message["text"])
                    event = loaded["event"]
                    payload = loaded["payload"]
                except (json.JSONDecodeError, KeyError):
                    continue  # wrong format, ignore for now. expose an error handler?
                else:
                    handler = self.event_router(event)
                    if handler:
                        ws.payload = payload
                        ws.event = event
                        if len(self.hooks.before_on) > 0:
                            await self.hooks.before_on[0](ws, handler)
                        else:
                            await handler(ws)
                        # after_on()?
            elif message["type"] == "websocket.disconnect":
                ws.code = message["code"]
                ws.connected = False
                for hook in self.hooks.on_disconnect:
                    await hook(ws)
                await ws.flush()
                return

    def add_event(self, event, func):
        self.event_router.add(event, func)

    async def connect_hook(self, ws):
        acceptance = dict(headers=[], subprotocol=None)
        if len(self.hooks.on_connect) > 0:
            await self.hooks.on_connect(ws, acceptance)
            if not acceptance:
                return None
        return acceptance["headers"], acceptance["subprotocol"]
