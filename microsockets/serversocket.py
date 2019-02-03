import asyncio
import json
from pubsub import pub

class ServerSocket(object):
    listeners = {}  # Need to store strong reference to these

    def __init__(self, websocket):
        self.__websocket = websocket

    def subscribe(self, topic):
        def listener(payload, source=None, include_self=True):
            print(include_self, source, self.__websocket)
            if not include_self and source == self.__websocket:
                return

            async def publish():
                await self.__websocket.send(json.dumps({
                    "topic": topic,
                    "payload": payload
                }))
            asyncio.ensure_future(publish())
        self.listeners[topic] = listener  # Store in dict so it is not garbage collected
        pub.subscribe(listener, topic)

    def publishToOthers(self, topic, payload):
        print(topic, payload)
        pub.sendMessage(
            topic,
            payload=payload,
            source=self.__websocket,
            include_self=False
        )
