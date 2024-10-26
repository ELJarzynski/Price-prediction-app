// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; // Importuj Vuex store

createApp(App)
  .use(store) // Dodaj Vuex store
  .use(router)
  .mount('#app');