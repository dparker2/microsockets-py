# Minimal example. Still need to document everything possible.
import json
import microsockets

app = microsockets.Application()


@app.hooks.before_on
async def load_payload(ws, func):
    ws.payload = json.loads(ws.payload)
    await func(ws)


# other hooks:
# @app.hooks.on_startup
# @app.hooks.on_shutdown
# @app.hooks.on_connect
# @app.hooks.on_disconnect
# Use as many times as needed, functions
# called in the order they were added.


# Make a handler for the "join" event.
# Events routed to handlers by events.EventRouter, which can be subclassed/replaced
@app.on("join")
async def handle(ws):
    room = ws.payload["room"]
    user = ws.payload["user"]
    # Rooms managed by rooms.RoomManager, which can be subclassed/replaced
    await ws.join(room)
    # Emit event back to client, may pass a payload as second argument
    await ws.emit("joined")
    # Broadcast to all other users in the room. skip_self=False would send it to current client as well.
    await ws.broadcast("user joined", json.dumps(dict(user=user)), to=[room])
