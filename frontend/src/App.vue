<template>
  <router-view/>
  <meta name="csrf-token" content="{{ csrf_token }}">

</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      showMobileMenu: false,
      cart: {
        items: []
      },
      refreshPage() {
        window.location.reload();
    },
      user: null // Dodaj pole user do danych komponentu
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
    this.fetchUserData(); // Wywołaj metodę fetchUserData po zamontowaniu komponentu
    document.title = "OtoPrice"
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
      setTimeout(() => {
        window.location.reload(); // Odśwież /log-in
      }, 2);
    },
    async fetchUserData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/user/profile/');
        this.user = response.data;
      } catch (error) {
        console.error('Błąd podczas pobierania danych użytkownika:', error);
      }
    }
  },
  
  computed: {
      cartTotalLength() {
          let totalLength = 0

          for (let i = 0; i < this.cart.items.length; i++) {
              totalLength += this.cart.items[i].quantity
          }

          return totalLength
      }
  }
}
</script>
<style>
/* Global styles to ensure full height */
html, body, #app, router-view {
    height: 100%;
    margin: 0;
    padding: 0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
</style>