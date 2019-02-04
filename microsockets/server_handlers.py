class Handlers(object):
    handlers = {}

    def register(self, *, key):
        def decorator(handler):
            self.handlers[key] = handler
        return decorator
