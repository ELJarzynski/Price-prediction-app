<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="home">
        <header class="header">
            <router-link to="/" class="logo">OtoPrice</router-link>
            <nav class="nav">
                <!-- Sekcja warunkowa dla zalogowanych użytkowników -->
                <template v-if="$store.state.isAuthenticated">
                    <span v-if="user" class="user-name">{{ user.first_name }} {{ user.last_name }}</span>
                    <button @click="logout" class="button-app is-lighty logout-button">Wyloguj</button>
                </template>
            </nav>
        </header>
        <div class="content">
            <h1>OSZACUJ CENĘ MIESZKANIA</h1>
            <p>Użyj naszego algorytmu do sprawdzenia wartości mieszkania w mniej niż minutę <br>Dowiedz się ile mieszkanie może być warte</p>
            <div class="margin">
                <!-- Sekcja dla przycisków wyświetlanych po zalogowaniu -->
                <template v-if="$store.state.isAuthenticated">
                    <router-link to="/price" class="button-panel">PREDYKCJA CEN</router-link>
                    <router-link to="/tables" class="button-panel">PANEL UŻYTKOWNIKA</router-link>
                </template>
                <!-- Sekcja warunkowa dla niezalogowanych użytkowników -->
                <template v-else>
                    <router-link to="/log-in" class="button-login">ZALOGUJ SIĘ</router-link>
                    <router-link to="/sign-up" class="button-login">ZAŁÓŻ KONTO</router-link>
                </template>
            </div>
        </div>
    </div>
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
        this.fetchUserData();
    },
    methods: {
        async logout() {
            try {
                localStorage.removeItem('token'); // Usuń token
                this.$store.commit('SET_AUTH', false); // Ustaw stan autoryzacji w Vuex
                this.$router.push('/'); // Przekieruj na stronę główną
                setTimeout(() => {
                    window.location.reload(); // Odśwież stronę
                }, 2);
            } catch (error) {
                console.error('Błąd podczas wylogowywania:', error);
            }
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

<style scoped src="../style/home.css"></style>
