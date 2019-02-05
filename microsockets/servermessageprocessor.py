import json

class MessageProcessor(object):
    def __init__(self, key='type'):
        self.key = key


    def extract_handler_arguments(self, message):
        parsed = json.loads(message)
        return parsed[self.key], parsed