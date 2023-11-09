<template>
    <div class="container">
        <header class="page-header">
            <a class="page-header-logo-link" :href="getAttUrl() + '/'">
                <img class='page-header-logo' src="icons/header-logo.png" width="50" height="50" alt="Логотип FindGun.">
                <text class="logo-text">FindGun</text>
            </a>
            <div class='input-container'>
                <a class="site-link link-header archive"  :href="getAttUrl() + '/'">Работа с архивом</a>
                <a class="site-link link-header rtsp current-link" :href="getAttUrl() + '/rtsp'">Работа с RTSP</a>
            </div>
        </header>
        <main class="main-page">
            <h1 class="visually-hidden">Веб-сервис для поиска оружия на видео</h1>
            <section class="upload">
                <h2 class="page-title">Введите ссылку на RTSP поток</h2>
                <p class="page-subtitle">Формат: rtsp://user:password@ip/</p>
                <div class="upload-file__wrapper">
                    <input class='url-input' type="text" placeholder="Ссылка" v-model="rtspUrl"/>
                    <div class="upload-button__container container-button">
                        <button class="site-button send-button" @click="stopStream">Остановить поток</button>
                        <button class="site-button send-button" @click="sendURL">Отправить ссылку</button>
                    </div>
                </div>
                <div class="video_board__wrapper">
                    <q-inner-loading :showing="stream_loading" style="position: absolute;">
                                <q-spinner-ball
                                    size="100px"
                                    color="dark"
                                />
                        </q-inner-loading>
                    <img @click="showDialogVideo()" id="stream" style="height: 100%; width: 100%; border-radius: 8px;" >
                </div>
                <div class="image_board__wrapper">
                    <div class="q-pa-md row items-start q-gutter-md">
                        <q-card class="my-card" v-for="image in video_images" :key="image.filename">
                            <q-item>
                                <q-item-section>
                                    <q-item-label class="card-title">{{ image.filename }}</q-item-label>
                                    <q-item-label caption >
                                        <template v-for="(word, index) in image.class" :key="index">
                                            <span :class="getClass(word)">{{ word }}</span>
                                            <span v-if="index < image.class.length - 1">, </span>
                                        </template>
                                    </q-item-label>
                                </q-item-section>
                            </q-item>
                            <img @click="showDialog(image)" :src="'data:image/jpeg;base64,' + image.img">
                        </q-card>
                    </div>
                </div>
            </section>
        </main>
    </div>


    <q-dialog
        v-model="showStream"
        auto-close
        transition-duration="300"
    >
        <section>
            <img
                :src="dialogStream"
                class="dialog-image"
                fit="scale-up"
            >
        </section>
    </q-dialog>

    <q-dialog
        v-model="dialog"
        auto-close
        transition-duration="300"
    >
        <q-img
            :src="dialogImgSrc"
            class="dialog-image"
            fit="scale-up"
        >
        </q-img>
    </q-dialog>
</template>

<script>

import { defineComponent, ref } from 'vue'
import { useModelStore } from 'stores/model.js'
import { useMainStore } from 'stores/main.js'
import { storeToRefs } from 'pinia'



export default defineComponent({
    name: 'IndexPage',

    setup() {
        const store = useModelStore();
        const mainStore = useMainStore();
        const {images, stream_loading, stream_status, video_images} = storeToRefs(store)
        let dialog = ref(false)
        let file_status = ref('Файл не выбран')
        let rtspUrl = ref('')
        let showStream = ref(false)
        let encode_frame_cam = ref('')
        let dialogStream = ref('')
        return {
            showStream,
            video_images,
            encode_frame_cam,
            stream_status,
            rtspUrl,
            file_status,
            images,
            stream_loading,
            store,
            dialog,
            dialogStream,
            img_name: ref(''),
            img_class: ref(''),
        }
    },
    created() {
        document.title = 'FindGun | RTSP';
    },
    methods: {
        getClass(word) {
            return word === "person" ? "green-text" : word === "weapon" ? "red-text" : "";
        },
        getAttUrl() {
            const { protocol, hostname, port, url } = window.location;
            return `${protocol}//${hostname}:${port}`;
        },
        getFrame() {
            setInterval(() => {
                let frame = this.store.takeFrame();
                if (frame !== undefined && frame !== ''){
                    this.encode_frame_cam = frame
                }
            }, 1);

        },
        showDialog: function (img) {
            if (!this.error) {
                this.img_name = img.filename
                this.img_class = img.class.join(', ')
                this.dialogImgSrc = 'data:image/jpeg;base64,' + img.img
                this.dialog = true
            }
        },
        showDialogVideo: function () {
            if (!this.error) {
                this.showStream = true
            }
        },
        isValidRTSP(url) {
            return url.startsWith('rtsp://');
        },
        async sendURL() {
            if (this.isValidRTSP(this.rtspUrl)) {
                this.store.sendURL(this.rtspUrl);
                this.store.startConsuming()
                this.getFrame()
            } else {
                this.$q.notify({
                    message: 'Некорректная RTSP-ссылка!',
                    type: 'negative',
                    color: 'negative',
                    position: 'center',
                    icon: 'warning',
                });
            }
        },
        async stopStream() {
            if (this.stream_status == false){
                this.$q.notify({
                    message: 'Поток еще не запущен!',
                    type: 'negative',
                    color: 'negative',
                    position: 'center',
                    icon: 'warning',
                });
            } else {
                this.store.stopStreaming('stop')
                this.stream_status = false
                let img = document.getElementById('stream')
                this.encode_frame_cam = ''
                this.$q.notify({
                    message: 'Поток остановлен!',
                    type: 'info',
                    color: 'positive',
                    position: 'center',
                    icon: 'warning',
                });
            }
        }
    },
    watch: {
        encode_frame_cam(newV) {
            if (newV !== ''){
                let new_src = "data:image/png;base64," + newV;
                let img = document.getElementById('stream')
                img.src = new_src
                this.dialogStream = new_src
                this.stream_loading = false

            }
        },
    }
})

</script>
