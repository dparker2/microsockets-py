from . import scopes
from . import events
from . import rooms
from . import hooks


class Application(object):
    def __init__(
        self, *, event_router=events.EventRouter, room_manager=rooms.RoomManager
    ):
        self.hooks = hooks.Hooks()
        self.__scopes = dict(
            lifespan=scopes.LifespanScope(hooks=self.hooks),
            websocket=scopes.WebsocketScope(
                event_router=event_router(),
                room_manager=room_manager(),
                hooks=self.hooks,
            ),
        )

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
