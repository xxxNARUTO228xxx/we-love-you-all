import { boot } from 'quasar/wrappers'
import { mande } from 'mande'
import { createUID } from 'boot/utils'
import ReconnectingWebSocket from 'reconnecting-websocket';

const API_ROOT = '/api/v1'
const api = mande(API_ROOT)


class WS {
    constructor(url, client_id) {
        this.client_id = client_id
        this.url = url
        this.connection = new ReconnectingWebSocket(`${this.url}/${this.client_id}`)

        this.connection.onopen = (e) => {
            console.log(e)
            console.log(`connected to ${this.url}, client: ${this.client_id}`)
        }

        this.connection.onerror = () => {
            console.log("Ошибка!");
        }

        this.connection.onclose = () => {
            console.log("Соединение разорвано.");
        }
    }

    sendMessage(event_name, data) {
        let msg = {
            event: event_name,
            data: data,
        }
        this.connection.send(JSON.stringify(msg));
    }

}

const client_id = createUID()
let host = window.location.host
if (process.env.DEV) {
    console.log(`I'm on a development build`)
    host = 'localhost:3000'
}
const WS_URL = `ws://${host}${API_ROOT}/ws`
let ws = new WS(WS_URL, client_id)


export default boot(({ app, router, store }) => {

    app.config.globalProperties.$mande = mande
    app.config.globalProperties.$api = api
    app.config.globalProperties.$ws = ws

})

export { API_ROOT, api, ws }
