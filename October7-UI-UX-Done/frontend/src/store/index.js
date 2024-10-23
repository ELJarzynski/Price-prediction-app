// src/store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: false,
    token: null,
    user: null,
    cart: {
      items: []
    }
  },
  mutations: {
    initializeStore(state) {
      const token = localStorage.getItem('token');
      if (token) {
        state.token = token;
        state.isAuthenticated = true;
      }
    },
    logout(state) {
      state.isAuthenticated = false;
      state.token = null;
      state.user = null;
      localStorage.removeItem('token');
    },
    setUser(state, user) {
      state.user = user;
    }
  },
  actions: {
    async fetchUserData({ commit }) {
      try {
        const response = await fetch('http://127.0.0.1:8000/user/profile/');
        const data = await response.json();
        commit('setUser', data);
      } catch (error) {
        console.error('Błąd podczas pobierania danych użytkownika:', error);
      }
    }
  }
});
