class CallableList(list):
    def __call__(self, item):
        self.append(item)
        return item


class Middleware(object):
    def __init__(self):
        self.before_on = CallableList()
