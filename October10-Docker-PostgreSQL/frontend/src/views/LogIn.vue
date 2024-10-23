<template>
  <div>
    <!-- Error Notification -->
    <div v-if="showErrorNotification" class="notification-container">
      <div class="notification">
  <div class="delete" @click="hideNotification">
    <ion-icon name="close-outline"></ion-icon> <!-- Użycie ikony krzyżyka -->
  </div>
  <div class="notification-content">
    <p class="notification-message">
      Błędne dane, sprawdź je dane i spróbuj ponownie.
    </p>
  </div>
</div>
    </div>

    <header class="header">
      <router-link to="/" class="logo">OtoPrice</router-link>
      <nav class="nav">
        <template v-if="$store.state.isAuthenticated">
          <router-link to="/price" class="button-app is-lighty logout-button">Predykcja cen</router-link>
          <router-link to="/tables" class="button-app is-lighty logout-button">Panel użytkownika</router-link>
          <button @click="logout" class="button-app is-lighty logout-button">Wyloguj</button>
        </template>
        <template v-if="!$store.state.isAuthenticated">
          <router-link to="/log-in" class="button-app is-lighty logout-button">Zaloguj się</router-link>
          <router-link to="/sign-up" class="button-app is-lighty logout-button">Zarejestruj się</router-link>
        </template>
      </nav>
    </header>

    <section class="home">
      <div class="content">
        <div class="margin">
          <h2>Know Property Worth</h2>
          <p>OtoPrice to unikatowe narzędzie 
            pozwalające na natychmiastowe oszacowanie wartości indywidualnych lokali mieszkalnych 
            przy pomocy zaawansowanego modelu opartego na rozwiązaniach machine-learning. Opracowanego przez studenta UWM.</p>
        </div>
      </div>
      <div v-if="!$store.state.isAuthenticated" class="wrapper-login">
        <h2>Member login</h2>
        <form @submit.prevent="login">
          <div class="input-box">
            <span class="icon"><ion-icon name="mail-outline"></ion-icon></span>
            <input type="email" v-model="loginForm.email" required placeholder=" ">
            <label>Enter your email</label>  
          </div>
          <div class="input-box">
            <span class="icon"><ion-icon name="lock-closed-outline"></ion-icon></span>
            <input type="password" v-model="loginForm.password" required placeholder=" ">
            <label>Enter your password</label>  
          </div>
          <div class="remember-forgot">
            <label><input type="checkbox">
            Remember me</label>
            <a href="#">Forgot password</a>
          </div>
          <button type="submit" class="btn">Zaloguj</button>
          <div class="register-container">
            <p>Nie posiadasz konta? <router-link to="/sign-up" class="register-link">Zarejestruj się!</router-link></p>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  mounted() {

    const scriptModule = document.createElement('script');
    scriptModule.type = 'module';
    scriptModule.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js';
    document.body.appendChild(scriptModule);

    const scriptNomodule = document.createElement('script');
    scriptNomodule.nomodule = true;
    scriptNomodule.src = 'https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js';
    document.body.appendChild(scriptNomodule);
  },
  name: 'LogIn',
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      },
      showSuccessNotification: false,
      showErrorNotification: false
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user/token/', this.loginForm);
        
        const token = response.data.token;
        localStorage.setItem('token', token); // Zapisz token w localStorage
        console.log('Login successful');
        console.log(token);

        this.$store.commit('SET_AUTHENTICATED', true); // Aktualizuj stan w store
        this.showSuccessNotification = true;
        this.goToUserPanel(); // Przekieruj bezpośrednio po udanym logowaniu
      } catch (error) {
        console.error('Login error:', error.response.data);
        this.showErrorNotification = true;
      }
    },
    logout() {
      localStorage.removeItem('token'); // Usuń token z localStorage
      this.$store.commit('SET_AUTHENTICATED', false); // Zaktualizuj stan w store
      this.$router.push('/'); // Przekieruj na stronę główną
    },
    hideNotification() {
      this.showSuccessNotification = false;
      this.showErrorNotification = false;
    },
    goToUserPanel() {
      this.$router.push('/'); // Przekieruj do /user-main
      setTimeout(() => {
        window.location.reload(); // Odśwież /user-main
      }, 1000);
    }
  }
};
</script>

<style scoped src="../style/LogIn.css"></style>
