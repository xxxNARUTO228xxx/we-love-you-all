<template>
    <q-layout view="lhr lpR lFr">

        <!-- <q-drawer
            v-model="leftDrawerOpen"
            show-if-above
            side="left"
            bordered
            :mini="miniState"
            @mouseover="miniState = false"
            @mouseout="miniState = true"
            :width="200"
            :breakpoint="500"
            class="bg-grey-3"
        >
            <q-list>
                <EssentialLink
                    v-for="link in essentialLinks"
                    :key="link.title"
                    v-bind="link"
                />
            </q-list>
        </q-drawer> -->

        <q-page-container>
            <router-view />
        </q-page-container>

    </q-layout>

</template>

<script>
import { defineComponent, ref } from 'vue'
// import EssentialLink from 'components/EssentialLink.vue'
import { useMainStore } from 'stores/main'
import { storeToRefs } from 'pinia'
import { useQuasar } from "quasar";

const linksList = [
    {
        title: 'Отчет',
        caption: 'report',
        icon: 'leaderboard',
        link: '/'
    },
]

export default defineComponent({
    name: 'MainLayout',

    // components: {
    //     EssentialLink
    // },

    setup() {
        const leftDrawerOpen = ref(false)
        const mainStore = useMainStore()
        const { errorMessage, okMessage } = storeToRefs(mainStore)

        // const $q = useQuasar()
        // console.log($q.dark.mode) // "auto", true, false
        // $q.dark.set(true)


        return {
            drawer: ref(false),
            miniState: ref(true),
            essentialLinks: linksList,
            leftDrawerOpen,
            errorMessage,
            okMessage,
            toggleLeftDrawer() {
                leftDrawerOpen.value = !leftDrawerOpen.value
            }
        }
    },

    watch: {
        errorMessage(newMessage) {
            if (newMessage !== '') {
                this.$q.notify({
                    type: 'negative',
                    message: 'Ошибка.',
                    caption: newMessage,
                    position: 'center',
                    multiLine: true,
                    timeout: 10000,
                    closeBtn: true,
                })
            }

        },
        okMessage(newMessage) {
            if (newMessage !== '') {
                this.$q.notify({
                    type: 'info',
                    message: 'Ok.',
                    caption: newMessage,
                    position: 'center',
                    multiLine: true,
                    timeout: 10000,
                    closeBtn: true,
                })
            }

        }
    }
})
</script>
