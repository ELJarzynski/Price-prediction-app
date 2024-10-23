<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <header class="header">
    <router-link to="/" class="logo">OtoPrice</router-link>
    <nav class="nav">
      <!-- Sekcja warunkowa dla zalogowanych użytkowników -->
      <template v-if="$store.state.isAuthenticated">
        <router-link to="/price" class="button-app is-lighty logout-button">Predykcja cen</router-link>
        <router-link to="/tables" class="button-app is-lighty logout-button">Panel użytkownika</router-link>
        <button @click="logout" class="button-app is-lighty logout-button">Wyloguj</button>
      </template>
      <!-- Sekcja warunkowa dla niezalogowanych użytkowników -->
      <template v-if="!$store.state.isAuthenticated">
        <router-link to="/log-in" class="button-app is-lighty logout-button">Zaloguj się</router-link>
        <router-link to="/sign-up" class="button-app is-lighty logout-button">Zarejestruj się</router-link>
      </template>
    </nav>
  </header>
  <div class="home">
    <div class="content">
      <div class="margin">
        <h2>Know Property Worth</h2>
        <p>OtoPrice to unikatowe narzędzie 
          pozwalające na natychmiastowe oszacowanie wartości indywidualnych lokali mieszkalnych 
          przy pomocy zaawansowanego modelu opartego na rozwiązaniach machine-learning. Opracowanego przez studenta UWM.</p>
      </div>
    </div>
    <div class="wrapper-login">
      <h2>Zarejestruj się</h2>
      <form @submit.prevent="register">
        <div class="input-box">
          <span class="icon"><ion-icon name="mail-outline"></ion-icon></span>
          <input type="email" v-model="registerForm.email" required placeholder=" ">
          <label>E-mail</label>
        </div>
        <div class="input-box">
          <span class="icon"><ion-icon name="person-outline"></ion-icon></span>
          <input type="text" v-model="registerForm.first_name" required placeholder=" ">
          <label>Imię</label>
        </div>
        <div class="input-box">
          <span class="icon"><ion-icon name="person-outline"></ion-icon></span>
          <input type="text" v-model="registerForm.last_name" required placeholder=" ">
          <label>Nazwisko</label>
        </div>
        <div class="input-box">
          <span class="icon"><ion-icon name="lock-closed-outline"></ion-icon></span>
          <input type="password" v-model="registerForm.password" required placeholder=" ">
          <label>Hasło</label>
        </div>
        <button type="submit" class="btn">Zarejestruj</button>
      </form>
      <div class="register-container">
        <p>Masz już konto? <router-link to="/log-in" class="register-link">Zaloguj się!</router-link></p>
      </div>
    </div>
    <div v-if="showNotification" class="notification-container">
      <div class="notification is-success">
        <button class="delete" @click="hideNotification"></button>
        Rejestracja udana! <i class="fas fa-check-circle"></i>
      </div>
    </div>
    <!-- Sekcja błędów rejestracji -->
    <div v-if="showErrorNotification" class="notification-container">
      <div class="notification is-danger">
        <button class="delete" @click="hideNotification"></button>
        <p class="notification-message">
          Błąd rejestracji!
          <br>
          Sprawdź swoje dane i spróbuj ponownie.
        </p>
      </div>
    </div>
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
  name: 'SignUp',
    data() {
      return {
        registerForm: {
          email: '',
          first_name: '',
          last_name: '',
          password: ''
        },
        showNotification: false
      };
    },
    methods: {
      async register() {
        this.errors = [];
  
        if (!this.errors.length) {
          try {
            const response = await axios.post('http://127.0.0.1:8000/user/create/', this.registerForm);
            console.log(response.data);
            await this.loginAfterRegistration(response.data.token);
            this.clearForm();
            this.$router.push('/');
          } catch (error) {
            console.error('Registration error:', error.response.data);
          }
        }
      },
      // eslint-disable-next-line no-unused-vars
      async loginAfterRegistration(token) {
        try {
          const loginResponse = await axios.post('http://127.0.0.1:8000/user/token/', {
            email: this.registerForm.email,
            password: this.registerForm.password
          });
  
          const authToken = loginResponse.data.token;
          localStorage.setItem('token', authToken);
          this.$router.push('/user-main');
        } catch (error) {
          console.error('Login error after registration:', error.response.data);
        }
      },
      clearForm() {
        this.registerForm.email = '';
        this.registerForm.first_name = '';
        this.registerForm.last_name = '';
        this.registerForm.password = '';
      },
      passwordType() {
      },
      hideNotification() {
        this.showNotification = false;
      },
    }
  };
  </script>

<style scoped src="../style/signup.css"></style>
