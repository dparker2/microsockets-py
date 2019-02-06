import asyncio
import json
from pubsub import pub

class ServerSocket(object):
    listeners = {}  # Need to store strong reference to these


    def __init__(self, websocket):
        self.__websocket = websocket


    def subscribe(self, topic):
        # Make a new function for each subscribe
        def listener(payload, tasks=[], source=None, include_self=True):
            if not include_self and source == self.__websocket:
                return

            async def publish():
                await self.__websocket.send(json.dumps({
                    "topic": topic,
                    "payload": payload
                }))
            # Add the websocket send tasks to the event loop and tasks variable passed
            tasks.append(asyncio.ensure_future(publish()))

        if self.__websocket not in self.listeners:
            self.listeners[self.__websocket] = {}
        self.listeners[self.__websocket][topic] = listener  # Store in dict so it is not garbage collected

        pub.subscribe(listener, topic)


    def unsubscribe(self, topic):
        # Removing the reference to the listener will cause it to be garbage collected
        if self.__websocket in self.listeners and topic in self.listeners[self.__websocket]:
            del self.listeners[self.__websocket][topic]


    def unsubscribe_all(self):
        if self.__websocket in self.listeners:
            del self.listeners[self.__websocket]


    async def publish_to_others(self, topic, payload):
        publishes = []
        pub.sendMessage(
            topic,
            payload=payload,
            tasks=publishes,
            source=self.__websocket,
            include_self=False
        )
        return asyncio.gather(*publishes)
