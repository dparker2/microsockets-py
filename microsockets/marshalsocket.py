import json

class SocketUnmarshaller(object):
    def __init__(self):
        self.key = 'type'


    def extract_handler_arguments(self, message):
        parsed = json.loads(message)
        arg = parsed['data'] if 'data' in parsed else None
        return parsed[self.key], arg


class SocketMarshaller(object):
    def __init__(self):
        self.key = 'type'


    def to_string(self, key, message):
        return json.dumps({
            self.key: key,
            'data': message
        })