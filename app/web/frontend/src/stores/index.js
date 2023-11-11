import { store } from 'quasar/wrappers'
import { createPinia } from 'pinia'
import { ws } from 'boot/api'

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */


function WSPlugin() {
    return { ws }
}

export default store((/* { ssrContext } */) => {
    const pinia = createPinia()
    pinia.use(WSPlugin)

    return pinia
})
