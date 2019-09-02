class EventRouter(object):
    def __init__(self):
        self.__events = dict()

    def __call__(self, event: str):
        return self.__events.get(event)

    def add(self, event: str, func):
        self.__events[event] = func
