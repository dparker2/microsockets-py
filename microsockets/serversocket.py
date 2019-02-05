import asyncio
import json
from pubsub import pub

class ServerSocket(object):
    listeners = {}  # Need to store strong reference to these


    def __init__(self, websocket):
        self.__websocket = websocket


    def subscribe(self, topic):
        def listener(payload, source=None, include_self=True):
            if not include_self and source == self.__websocket:
                return

            async def publish():
                await self.__websocket.send(json.dumps({
                    "topic": topic,
                    "payload": payload
                }))
            asyncio.ensure_future(publish())

        if self.__websocket not in self.listeners:
            self.listeners[self.__websocket] = {}
        self.listeners[self.__websocket][topic] = listener  # Store in dict so it is not garbage collected

        pub.subscribe(listener, topic)


    def unsubscribe(self, topic):
        # Removing the reference to the listener will cause it to be garbage collected
        del self.listeners[self.__websocket][topic]


    def unsubscribe_all(self):
        if self.__websocket in self.listeners:
            del self.listeners[self.__websocket]


    def publish_to_others(self, topic, payload):
        pub.sendMessage(
            topic,
            payload=payload,
            source=self.__websocket,
            include_self=False
        )
