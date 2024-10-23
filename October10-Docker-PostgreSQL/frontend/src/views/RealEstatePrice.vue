<template>
  <div class="home">
    <header class="header">
      <router-link to="/" class="logo">OtoPrice</router-link>
      <nav class="nav">
        <template v-if="$store.state.isAuthenticated">
          <span v-if="user" class="user-name">{{ user.first_name }} {{ user.last_name }}</span>
          <router-link to="/price" class="button-app is-lighty logout-button">Predykcja cen</router-link>
          <router-link to="/tables" class="button-app is-lighty logout-button">Panel użytkownika</router-link>
          <button @click="logout" class="button-app is-lighty logout-button">Wyloguj</button>
        </template>
        <template v-if="!$store.state.isAuthenticated">
          <router-link to="/log-in" class="button-app is-lighty logout-button">Log In</router-link>
          <router-link to="/sign-up" class="button-app is-lighty logout-button">Sign Up</router-link>
        </template>
      </nav>
    </header>

    <div class="form-panel">
      <h1>Oszacuj wartość mieszkania</h1>
      <form @submit.prevent="createProperty" class="create-property-form">
        <div class="form-group">
          <label for="squareMeters">Metry kwadratowe:</label>
          <input type="number" id="squareMeters" v-model="newProperty.square_meters" class="form-control" min="10" max="1000" step="1">
          <span>{{ newProperty.square_meters }} m²</span>
        </div>
        <div class="form-group">
          <label for="bedrooms">Sypialnie:</label>
          <input type="number" id="bedrooms" v-model="newProperty.bedrooms" class="form-control" min="0" max="10" step="1">
        </div>
        <div class="form-group">
          <label for="bathrooms">Łazienki:</label>
          <input type="number" id="bathrooms" v-model="newProperty.bathrooms" class="form-control" min="0" max="10" step="1">
        </div>
        <div class="form-group">
          <label for="neighborhood">Osiedle:</label>
          <select id="neighborhood" v-model="newProperty.neighborhood" class="form-control">
            <option value="">Wybierz Okolice</option>
            <option value="Rural">Wioska</option>
            <option value="Suburb">Przedmieścia</option>
            <option value="Urban">Miejski</option>
          </select>
        </div>
        <div class="form-group">
          <label for="yearBuilt">Rok Budowy:</label>
          <input type="number" id="yearBuilt" v-model="newProperty.year_built" class="form-control"  min="1950" max="2024" step="1">
        </div>
        <div class="buttons">
          <button type="button" @click="convertAndPredictPrice" class="price-dis">Oszacuj Cenę</button>
          <span v-if="newProperty.price" class="price-display">Oszacowana cena: <br> {{ newProperty.price  }} PLN</span>
          <button type="submit" class="price-dis">Zapisz Nieruchomość</button>
        </div>
      </form>
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  mounted() {
    this.setCsrfToken();
  },
  name: 'CreateProperty',
  data() {
    return {
      newProperty: {
        square_meters: 100, // Używamy metrów kwadratowych
        bedrooms: '',
        bathrooms: '',
        neighborhood: '',
        year_built: '',
        price: ''
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    setCsrfToken() {
      const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
      if (csrfMetaTag) {
        const csrfToken = csrfMetaTag.getAttribute('content');
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
      } else {
        console.error('CSRF token meta tag not found.');
      }
    },

    // Przelicza metry kwadratowe na stopy kwadratowe i wywołuje predykcję
    async convertAndPredictPrice() {
      try {
        const squareFeet = this.newProperty.square_meters * 10.7639; // Przeliczenie na stopy kwadratowe
        const neighborhood = this.newProperty.neighborhood;
        const neighborhoodRural = neighborhood === 'Rural' ? 1 : 0;
        const neighborhoodSuburb = neighborhood === 'Suburb' ? 1 : 0;
        const neighborhoodUrban = neighborhood === 'Urban' ? 1 : 0;

        const response = await axios.post('http://127.0.0.1:8000/property/predict_price/', {
          square_feet: parseInt(squareFeet, 10), // Używamy przeliczonych wartości
          bedrooms: parseInt(this.newProperty.bedrooms, 10),
          bathrooms: parseInt(this.newProperty.bathrooms, 10),
          year_built: parseInt(this.newProperty.year_built, 10),
          neighborhood_rural: neighborhoodRural,
          neighborhood_suburb: neighborhoodSuburb,
          neighborhood_urban: neighborhoodUrban
        });

        this.newProperty.price = parseInt(response.data.predicted_price * 4.20, 10); // Wyświetlanie oszacowanej ceny

      } catch (error) {
        console.error('Error predicting price:', error);
      }
    },

    async createProperty() {
      this.successMessage = '';
      this.errorMessage = '';

      try {
        if (this.validateForm()) {
          await this.convertAndPredictPrice();
          if (this.newProperty.price) {
            const response = await axios.post('http://127.0.0.1:8000/property/create_property/', {
              square_feet: parseInt(this.newProperty.square_meters * 10.7639, 10), // Przeliczenie metrów na stopy
              bedrooms: parseInt(this.newProperty.bedrooms, 10),
              bathrooms: parseInt(this.newProperty.bathrooms, 10),
              neighborhood: this.newProperty.neighborhood,
              year_built: parseInt(this.newProperty.year_built, 10),
              price: parseInt(this.newProperty.price, 10)
            });

            this.successMessage = 'Posiadłość została zapisana pomyślnie!';
            console.log('Property created:', response.data);

            this.resetForm();
          } else {
            this.errorMessage = 'Failed to predict the price.';
          }
        } else {
          this.errorMessage = 'Proszę wypełnij brakujące pola.';
        }
      } catch (error) {
        console.error('Error creating property:', error.response ? error.response.data : error.message);
        this.errorMessage = 'An error occurred while creating the property.';
      }
    },

    validateForm() {
      return (
        this.newProperty.bedrooms &&
        this.newProperty.bathrooms &&
        this.newProperty.neighborhood &&
        this.newProperty.year_built
      );
    },

    resetForm() {
      this.newProperty = {
        square_meters: 100, // Resetowanie metrów kwadratowych
        bedrooms: '',
        bathrooms: '',
        neighborhood: '',
        year_built: '',
        price: ''
      };
    },
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
};
</script>

<style scoped src="../style/RealEstatePrice.css"></style>