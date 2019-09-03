import json


class Socket(object):
    def __init__(self, scope, send, room_manager):
        self.scope = scope
        self.connected = False
        self.payload = None
        self.event = None
        self.code = None
        self.__send = send
        self.__room_manager = room_manager

    async def emit(self, event, payload: str = ""):
        await self.__send(
            dict(
                type="websocket.send",
                text=json.dumps(dict(event=event, payload=payload)),
            )
        )

    async def broadcast(self, event, payload, to=[], skip_self=True):
        for room in to:
            for socket in await self.__room_manager.members(room):
                if skip_self and socket == self:
                    continue
                if socket.connected == False:
                    continue
                await socket.__send(
                    dict(
                        type="websocket.send",
                        text=json.dumps(dict(event=event, payload=payload)),
                    )
                )

    async def join(self, room: str):
        await self.__room_manager.join(room, self)

    async def rooms(self):
        return await self.__room_manager.rooms(self)

    async def close(self):
        self.connected = False
        await self.flush()
        await self.__send(dict(type="websocket.close", code=self.code))

    async def flush(self):
        await self.__room_manager.flush(self)

    # process this event
    # ws.scope <-- asgi scope object
    # ws.emit("event", "")
    # ws.broadcast("event", "", to=["room"])
    # ws.payload <-- payload received, str
    # ws.event <-- exact event emitted, str
    # ws.code <-- code set on disconnect, can be seen in on_disconnect. or set before closing connection to send to client.
    # ws.close <-- close connection. send ws.code or 1000 by default as code
    # ws.join <-- subscribe to room
    # ws.leave <-- unsubscribe from room
    # ws.rooms <-- list of subscribed rooms
