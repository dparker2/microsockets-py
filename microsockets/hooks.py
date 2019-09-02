class CallableList(list):
    def __call__(self, item):
        self.append(item)
        return item


class Hooks(object):
    def __init__(self):
        self.before_on = CallableList()
        self.on_startup = CallableList()
        self.on_shutdown = CallableList()
        self.on_connect = CallableList()
        self.on_disconnect = CallableList()
