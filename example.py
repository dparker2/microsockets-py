from microsockets import MicroServer, Handlers

# Handlers is used to register handlers which are later registered
# by MicroServer.register_handlers(), allowing handlers to be
# registered in separate files.
handlers = Handlers()


@handlers.register(key='SubChannel')
async def sub_channel_message_handler(websocket, message):
    topic = '{}.{}'.format(message['server'], message['channel'])
    websocket.subscribe(topic)


@handlers.register(key='NewMessage')
async def new_message_handler(websocket, message):
    topic = '{}.{}.NewMessage'.format(message['server'], message['channel'])
    websocket.publish_to_others(topic, message)
    return True

app = MicroServer()
app.register_handlers(handlers)


# Message handlers can also be registered directly on the MicroServer
# instance itself.
@app.register(key='LeaveChannel')
async def leave_channel_handler(websocket, message):
    topic = '{}.{}'.format(message['server'], message['channel'])
    websocket.unsubscribe(topic)


if __name__ == '__main__':
    app.run()
