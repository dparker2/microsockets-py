from . import scopes
from . import events


class Application(object):
    def __init__(self):
        websocket_scope = scopes.WebsocketScope(events.EventRouter())

        self.middleware = websocket_scope.middleware
        self.__scopes = dict(lifespan=scopes.LifespanScope(), websocket=websocket_scope)

    async def __call__(self, scope, receive, send):
        try:
            scope_handler = self.__scopes[scope["type"]]
        except KeyError:
            pass
        else:
            await scope_handler(scope, receive, send)

    def on(self, event):
        def decorator(func):
            self.__scopes["websocket"].add_event(event, func)
            return func

        return decorator
