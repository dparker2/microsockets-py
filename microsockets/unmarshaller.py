import json

class Unmarshaller(object):
    def __init__(self, key='type'):
        self.key = key


    def get_handler_arguments(self, message):
        parsed = json.loads(message)
        return parsed[self.key], parsed
