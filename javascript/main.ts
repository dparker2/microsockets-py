export default class MicroSocket extends WebSocket {
    listeners: { [key: string]: Function[]; }

    constructor(url: string, protocols: string | string[]) {
        super(url, protocols);
        this.listeners = {};
        this.addEventListener('message', wsEvent => {
            const { event, payload } = JSON.parse(wsEvent.data);
            const listeners = this.listeners[event]
            if (listeners) {
                listeners.forEach(listener => {
                    listener(payload, event, wsEvent)
                });
            }
        })
    }

    on(event: string, callback: Function) {
        if (!this.listeners[event]) {
            this.listeners[event] = []
        } else {
            this.listeners[event].push(callback)
        }
    }

    off(event: string, callback: Function) {
        const listeners = this.listeners[event];
        if (!listeners) {
            return;
        }
        if (callback) {
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        } else {
            delete this.listeners[event];
        }
    }

    send(payload: string, event: string = "") {
        const data = JSON.stringify({ event, payload })
        super.send(data)
    }
}
