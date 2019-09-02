import json
from collections import defaultdict

_rooms = defaultdict(list)


class Socket(object):
    def __init__(self, scope, send):
        self.scope = scope
        self.payload = None
        self.event = None
        self.__send = send

    async def emit(self, event, payload: str):
        await self.__send(
            dict(
                type="websocket.send",
                text=json.dumps(dict(event=event, payload=payload)),
            )
        )

    async def broadcast(self, event, payload, to=[]):
        for room in to:
            for socket in _rooms[room]:
                await socket.__send(
                    dict(
                        type="websocket.send",
                        text=json.dumps(dict(event=event, payload=payload)),
                    )
                )

    def join(self, room: str):
        _rooms[room].append(self)

    # process this event
    # ws.scope <-- asgi scope object
    # ws.emit("event", "")
    # ws.broadcast("event", "", to=["room"])
    # ws.payload <-- payload received
    # ws.event <-- exact event emitted
