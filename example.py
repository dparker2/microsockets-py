from microsockets import MicroServer

app = MicroServer()


@app.register(key='NewMessage')
async def new_message_handler(websocket, message):
    topic = '{}.{}.NewMessage'.format(message['server'], message['channel'])
    websocket.publish_to_others(topic, message['body'])
    return {"response":"test"}


@app.register(key='SubChannelMessage')
async def sub_channel_message_handler(websocket, message):
    topic = '{}.{}.NewMessage'.format(message['server'], message['channel'])
    websocket.subscribe(topic)


if __name__ == '__main__':
    app.run()
