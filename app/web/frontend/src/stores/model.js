import { defineStore } from 'pinia';
import { api, API_ROOT } from 'boot/api';
import { useMainStore } from './main';
import { createUID} from 'boot/utils'

let frame_cam = ''

export const useModelStore = defineStore('model', {
    state: () => ({
        loading: false,
        load_progress: false,
        progress: 0,
        stream_loading: false,
        stream_status: false,
        images: [],
        video_images: [],
        download_url: '',
        client_id: createUID()
    }),

    actions: {
        async stopStreaming(str){
            const mainStore = useMainStore()
            try {
                const query = {
                    query: str,
                }
                const data = await api.get('/model/rtsp_stop', { query: query })
                let { items } = data
                this.stream_status = false
                mainStore.errorMessage = '';
            } catch (error) {
                console.log('ERROR', error);
                console.dir(error)
                mainStore.errorMessage = error.message
                return error
            }
        },
        async downloadImage(filename){
            const mainStore = useMainStore()
            try {
                const data = await fetch(`${API_ROOT}/model/get_image?filename=${filename}`, {
                    method: 'GET',
                });
                const imgBlob = await data.blob();
                const imageUrl = URL.createObjectURL(imgBlob);
                mainStore.errorMessage = '';
                return imageUrl
            } catch (error) {
                console.log('ERROR', error);
                console.dir(error)
                mainStore.errorMessage = error.message
                return error
            }

        },
        async sendURL(RtspUrl){
            console.log(RtspUrl)
            const mainStore = useMainStore()

            try {
                this.stream_loading = true;
                const query = {
                    rtsp_url: RtspUrl,
                }
                const data = await api.get('/model/rtsp', { query: query })
                let { items } = data
                this.stream_status = true
                mainStore.errorMessage = '';
            } catch (error) {
                console.log('ERROR', error);
                console.dir(error)
                mainStore.errorMessage = error.message
                return error
            }
        },

        async getData(archive) {

            const mainStore = useMainStore()

            try {
                console.log(archive)
                this.loading = true;
                this.load_progress = true;
                const formData = new FormData();
                formData.append('file', archive);
                const resp = await fetch(`${API_ROOT}/model/archive`, {
                    method: 'POST',
                    body: formData,
                  });
                mainStore.errorMessage = '';
                if (resp.ok) {
                    const videoBlob = await resp.blob();
                    const videoUrl = URL.createObjectURL(videoBlob);
                    this.download_url = videoUrl
                    this.progress = 1
                    this.load_progress = false
                }
            } catch (error) {
                console.log('ERROR', error);
                console.dir(error)
                mainStore.errorMessage = error.message
                return error
            }
        },
        takeFrame(){
            if (frame_cam !== '' && frame_cam !== undefined){
                return frame_cam
            }
        },
        async getFrame(frame){
            frame_cam = frame
        },
        async startConsuming() {
            console.log('start consuming');
            this.ws.connection.onmessage = (evt) => {
                let e_data = JSON.parse(evt.data)
                let { event, data } = e_data
                if (event == 'new_frame') {
                    let frame = data
                    this.getFrame(frame)
                }
                if (event == 'weapon_detect') {
                    let frame_data = data
                    this.video_images.push(frame_data)
                }
                if (event == 'video_weapon'){
                    let frame_video = data
                    console.log("!",frame_video)
                    this.loading = false;
                    this.images.push(frame_video)
                }
                if (event == 'progress'){
                    let progress_value = data
                    this.progress = progress_value['progress']
                }
                if (event == "reload") {
                    location.reload()
                }
            }
        },
        async sendEcho() {
            this.ws.sendMessage('echo', { 'msg': 'hello' })
        }
    },

});
