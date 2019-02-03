from microsockets import MicroServer

app = MicroServer()


@app.register(key='NewMessage')
async def newMessageHandler(websocket, message):
    topic = '{}.{}.NewMessage'.format(message['server'], message['channel'])
    websocket.publishToOthers(topic, message['body'])
    return {"response":"test"}


@app.register(key='SubChannelMessage')
async def subChannelMessageHandler(websocket, message):
    topic = '{}.{}.NewMessage'.format(message['server'], message['channel'])
    websocket.subscribe(topic)


if __name__ == '__main__':
    app.run()
