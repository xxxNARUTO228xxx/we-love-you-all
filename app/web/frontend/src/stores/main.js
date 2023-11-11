import { defineStore } from 'pinia';
import { api } from 'boot/api';

/*
 * Стор для хранения данных приложения
 * например ошибок
 */


export const useMainStore = defineStore('main', {
    state: () => ({
        errorMessage: '',
        okMessage: '',
    }),
});
