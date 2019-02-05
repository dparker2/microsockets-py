class Handlers(object):
    def __init__(self):
        self.handlers = {}

    def register(self, *, key):
        def decorator(handler):
            self.handlers[key] = handler
        return decorator
