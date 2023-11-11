<template>
    <div class="container">
        <header class="page-header">
            <a class="page-header-logo-link" :href="getAttUrl() + '/'">
                <img class='page-header-logo' src="icons/header-logo.png" width="50" height="50" alt="Логотип FindGun.">
                <text class="logo-text">FindGun</text>
            </a>
            <div class='input-container'>
                <a class="site-link link-header archive current-link"  :href="getAttUrl() + '/'">Работа с архивом</a>
                <a class="site-link link-header rtsp" :href="getAttUrl() + '/rtsp'">Работа с RTSP</a>
            </div>
        </header>
        <main class="main-page">
            <h1 class="visually-hidden">Веб-сервис для поиска оружия на видео</h1>
            <section class="upload">
                <h2 class="page-title">Загрузите архив с видео для поиска оружия (zip)</h2>
                <p class="page-subtitle">Формат видео должен быть .mp4, .wmv, .avi</p>
                <div class="upload-file__wrapper">
                    <label class="custom-file-input-label" for="file">Выберите файл</label>
                    <input class='upload-input' type="file" id="file" ref="file" style="display: none;" v-on:change="handleFileUpload()"/>
                    <p class="file-status">{{ file_status }}</p>
                    <div class="upload-button__container container-button">
                        <q-linear-progress stripe color='dark' size="10px" :value="progress"  style="width: 300px;"/>
                        <button class="site-button send-button arhive-button" @click="uploadFile">Отправить архив</button>
                    </div>
                </div>
                <div class="image_board__wrapper">
                    <div class="q-pa-md row items-start q-gutter-md">
                        <q-inner-loading :showing="loading" style="position: absolute;">
                                <q-spinner-ball
                                    size="100px"
                                    color="dark"
                                />
                        </q-inner-loading>
                        <q-card class="my-card" v-for="image in images" :key="image.filename">
                            <q-item>
                                <q-item-section class="big_window" style="min-height: 120px; align-items: flex-start">
                                    <q-item-label class="card-title">
                                        {{ image.filename }}
                                        <button class="edit_button" @click="downloadImageInfo(image)">
                                            <img src="icons/edit.svg" alt="SVG Icon" />
                                        </button>
                                    </q-item-label>
                                    <q-item-label caption >
                                        <template v-for="(word, index) in image.class" :key="index">
                                            <span :class="getClass(word)">{{ word }}</span>
                                            <span v-if="index < image.class.length - 1">, </span>
                                        </template>
                                    </q-item-label>
                                    <q-item-label caption >
                                        <template v-for="(word, index) in image.poses" :key="index">
                                            <span>{{ word }}</span>
                                            <span v-if="index < image.poses.length - 1">, </span>
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
        v-model="dialog"
        auto-close
        transition-duration="300"
        style="height: 100%; width:100%;"
    >
        <q-img
            :src="dialogImgSrc"
            class="dialog-image"
            style="height: 100%; min-width:1200px;"
            fit="scale-up"
        >
            <div class="absolute-bottom text-subtitle1 text-center">
                Название: {{ img_name }} <span> | </span> Класс: {{ img_class }}
            </div>
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
        const {images, loading, load_progress, progress, download_url} = storeToRefs(store)
        let selectedFile = ref(null)
        let dialog = ref(false)
        let file_status = ref('Файл не выбран')
        return {
            download_url,
            progress,
            load_progress,
            file_status,
            images,
            loading,
            selectedFile,
            store,
            dialog,
            dialogImgSrc: ref(''),
            img_name: ref(''),
            img_class: ref(''),
        }
    },
    created() {
        document.title = 'FindGun | Архив';
        this.store.startConsuming()
    },
    methods: {
        async downloadImageInfo(imageData){
            let image_url = await this.store.downloadImage(imageData.filename);
            const textContent = imageData.bboxes.join('\n');

            let blob = new Blob([textContent], { type: "text/plain" });
            let aImage = document.createElement("a");
            let a = document.createElement("a");
            let url = window.URL.createObjectURL(blob);
            aImage.href = image_url
            aImage.download = imageData.filename;
            a.href = url;
            let name = imageData.filename.slice(0, -4)
            a.download = `${name}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.appendChild(aImage);
            aImage.click();

            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            document.body.removeChild(aImage);

        },
        getClass(word) {
            return word === "person" ? "green-text" : word === "weapon" ? "red-text" : "";
        },
        getAttUrl() {
            const { protocol, hostname, port, url } = window.location;
            return `${protocol}//${hostname}:${port}`;
        },
        showDialog: function (img) {
            if (!this.error) {
                this.img_name = img.filename
                this.img_class = img.class.join(', ')
                this.dialogImgSrc = 'data:image/jpeg;base64,' + img.img
                this.dialog = true
            }
        },
        handleFileUpload() {
            let input = this.$refs.file;
            this.selectedFile = this.$refs.file.files[0];
            if (input.files.length > 0) {
                this.file_status = `${this.selectedFile['name']}`;
            } else {
                this.file_status = 'Файл не выбран';
            }
        },
        async uploadFile() {
            this.images = []
            this.progress = 0
            if (!this.selectedFile){
                this.$q.notify({
                        message: `Выберите файл !`,
                        type: 'negative',
                        color: 'negative',
                        position: 'center',
                        icon: 'warning',
                    })
            } else {
                let file_format = this.selectedFile['name'].slice(-3);
                if (file_format !== 'zip'){
                    this.selectedFile = null
                    this.$q.notify({
                        message: `Файл должен быть формата .zip !`,
                        type: 'negative',
                        color: 'negative',
                        position: 'center',
                        icon: 'warning',
                    })
                } else {
                    this.store.getData(this.selectedFile);
                }
            }
        },
    },
    watch: {
        download_url(newV){
            if (newV != ''){
                console.log('watch', newV)
                const a = document.createElement('a');
                a.href = newV;
                a.download = 'video.mp4';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        },
    },
})

</script>
