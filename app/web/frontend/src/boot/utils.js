import { boot } from 'quasar/wrappers'
import { date } from 'quasar'

function formatDateTime(dateStr, format = 'YYYY-MM-DD HH:mm:ss') {
    return date.formatDate(dateStr, format);
}

function formatDate(dateStr) {
    return date.formatDate(dateStr, 'YYYY-MM-DD');
}

function unixTsToDate(uts) {
    return new Date(uts * 1000)
}

function dtToUnixTs(dt) {
    return Math.floor(dt.getTime() / 1000)
}

function createUID() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

export default boot(({ app }) => {
    app.config.globalProperties.formatDateTime = formatDateTime
    app.config.globalProperties.formatDate = formatDate
    app.config.globalProperties.unixTsToDate = unixTsToDate

})


export { formatDateTime, formatDate, unixTsToDate, dtToUnixTs, createUID }
