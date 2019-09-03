# Microsockets

## ASGI Websocket Server made with simplicity in mind.

### Install
```bash
pip install microsockets
```

### Make an app
```python
import microsockets

app = microsockets.Application(
    # event_router, defaults to microsockets.events.EventRouter
    # room_manager, defaults to microsockets.rooms.RoomManager
)
```

### Add an event handler
```python
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
```

### Add middleware
```python
@app.hooks.before_on
async def load_payload(ws, func):
    ws.payload = json.loads(ws.payload)
    await func(ws)
```

### Run with ASGI Server
```bash
pip install uvicorn
```

```bash
uvicorn example:app
```

### Install JS client
```bash
npm install microsockets
```

### Make client side handlers and emit events
```javascript
import MicroSocket from microsockets;
const socket = MicroSocket("ws://127.0.0.1:8000");
// socket.on(event, handler): Add event handler
// socket.off(event, handler?): Remove event handler(s)
// socket.send(event, payload): Overridden WebSocket method, requires event. Payload defaults to "".

// MicroSocket returns a modified WebSocket, so the full WebSocket API is still available.
socket.onopen = function (e) {
    document.write("[open] Connection established <br />");
    document.write("Joining room <br />");
    socket.send("join", JSON.stringify({ room: "gamers", user: Math.random() }));
};

socket.on("joined", function (payload) {
    document.write(`[joined] Payload: ${payload} <br />`);
});

socket.on("user joined", function (payload) {
    document.write(`[user joined] Payload: ${payload} <br />`);
});
```

Run `example.py` and open `example.html` in multiple browser tabs to see this basic example.
