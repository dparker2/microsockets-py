from microsockets import MicroServer

app = MicroServer()

@app.register(key='NewMessage')
async def newMessageHandler(body):
    print(body)
    return {"response":"test"}

if __name__ == '__main__':
    app.run()
