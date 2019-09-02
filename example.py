import json
import microsockets

app = microsockets.Application()


@app.hooks.before_on
async def load_payload(ws, func):
    ws.payload = json.loads(ws.payload)
    await func(ws)


@app.on("topic")
async def handle(ws):
    # process this event
    # ws.scope <-- asgi scope object
    # ws.emit("event", "")
    # ws.join("room")
    # ws.broadcast("event", "", to=["room"])
    # ws.payload <-- payload received
    # ws.event <-- exact event emitted
    print(ws.payload)
    await ws.join("room1")
    await ws.emit("message", "received")
    await ws.broadcast("broadcast", "hello, everyone!", to=["room1"])
