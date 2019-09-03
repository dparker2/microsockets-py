interface MicroSocket extends WebSocket {
    on?: (event: string, callback: Function) => void;
    off?: (event: string, callback?: Function) => void;
    send: (payload: string, event?: string) => void;
}

export default function (url: string, protocols?: string | string[]) {
    const listeners: { [key: string]: Function[]; } = {};
    const websocket: MicroSocket = new WebSocket(url, protocols);

    websocket.on = function (event: string, callback: Function) {
        if (!listeners[event]) {
            listeners[event] = [callback]
        } else {
            listeners[event].push(callback)
        }
    }

    websocket.off = function (event: string, callback?: Function) {
        const funcs = listeners[event];
        if (!funcs) {
            return;
        }
        if (callback) {
            const index = funcs.indexOf(callback);
            if (index > -1) {
                funcs.splice(index, 1);
            }
        } else {
            delete listeners[event];
        }
    }

    websocket.send = function (event: string, payload: string = "") {
        const data = JSON.stringify({ event, payload })
        this.__proto__.send.call(this, data)
    }

    websocket.addEventListener('message', function (wsEvent) {
        const { event, payload } = JSON.parse(wsEvent.data);
        const funcs = listeners[event];
        if (funcs) {
            funcs.forEach(function (listener) {
                listener(payload, event, wsEvent);
            });
        }
    });

    return websocket;
}
