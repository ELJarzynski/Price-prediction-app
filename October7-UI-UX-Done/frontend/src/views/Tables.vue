<!-- eslint-disable vue/multi-word-component-names -->
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
          <router-link to="/log-in" class="button-app is-lighty logout-button">Zaloguj się</router-link>
          <router-link to="/sign-up" class="button-app is-lighty logout-button">Zarejestruj się</router-link>
        </template>
      </nav>
    </header>
  <div class="page-board">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Nieruchomości</h1>
      </div>
      <div class="column is-12 box">
        <table class="table is-fullwidth" v-if="boardTotalLength">
          <thead>
            <tr>
              <th>Metry Kwadratowe</th>
              <th>Sypialnie</th>
              <th>Łazienki</th>
              <th>Osiedle</th>
              <th>Rok Budowy</th>
              <th>Cena</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in boards" :key="item.id">
              <td>{{ Math.ceil(item.square_feet / 10.7639) }}</td>
              <td>{{ item.bedrooms }}</td>
              <td>{{ item.bathrooms }}</td>
              <td>{{ item.neighborhood }}</td>
              <td>{{ item.year_built }}</td>
              <td>{{ item.price }}</td>
              <td>
                <button @click="deleteBoard(item.id)" class="delete-button" style="margin-right: 10px;">Usuń</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>Nie posiadasz żadnej zapisanej nieruchomości ...</p>
      </div>
    </div>

    <!-- Modal do usuwania tablicy -->
    <transition name="fadeIn">
      <div v-if="deletepRropertyModalVisible" class="modal-delete">
        <div class="modal-content-delete">
          <h2 style="margin-bottom: 15px; font-weight: bold; font-size: 30px;">Usuń Nieruchomość</h2>
          <p>Czy napewno chcesz usunąć zapis tej nieruchomości?</p>
          <div class="buttons">
            <button @click="confirmDeleteBoard" class="delete-button">Tak</button>
            <button @click="cancelDeleteBoard" class="deny-button">Nie</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      square_feet: '',
      bedrooms: '',
      bathrooms: '',
      neighborhood: '',
      year_built: '',
      price: '',
      boards: [],
      // Delete
      propertyToDeleteId: null,
      deletepRropertyModalVisible: false,
      confirmRemoveModalActive: false,
    };
  },

  mounted() {
    this.fetchBoards();
  },

  methods: {
    // -------------------- FETCHE --------------------
    async fetchBoards() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/property/list_property/');
        this.boards = response.data;

        // Po pobraniu listy tablic, dla każdej tablicy pobierz liczbę użytkowników
        for (const board of this.boards) {
          await this.fetchBoardUsers(board.id);
        }
      } catch (error) {
        console.error('Error fetching boards:', error);
      }
    },




    // Delete
    async deleteBoard(propertyId) {
      try {
        this.deletepRropertyModalVisible = true;
        this.propertyToDeleteId = propertyId;
      } catch (error) {
        console.error('Error deleting board:', error);
      } 
    },

    async confirmDeleteBoard() {
      try {
        await axios.delete(`http://127.0.0.1:8000/property/${this.propertyToDeleteId}/delete_property/`);
        this.fetchBoards();
        this.closeDeleteBoardModal();
      } catch (error) {
        console.error('Error confirming deletion of board:', error);
      }
    },

    cancelDeleteBoard() {
      this.closeDeleteBoardModal();
    },

    closeDeleteBoardModal() {
      this.deletepRropertyModalVisible = false;
      this.propertyToDeleteId = null;
    },

    // Delete
   async deleteUserFromBoard(propertyId, user) {
      try {
        console.log("User:", user); // Dodajmy to logowanie
        //const userId = user.user_detail.id; // Pobierz user_id z obiektu user
        // Wykonanie zapytania HTTP do usunięcia użytkownika z tablicy
        await axios.delete(`http://127.0.0.1:8000/property/${propertyId}/delete_user/${this.removeUserId}`);

        // Pobranie zaktualizowanej listy użytkowników po usunięciu
        await this.fetchBoardUsersList(propertyId);
        window.location.reload();
      } catch (error) {
        console.error('Error deleting user from board:', error);
      }
    },

    async removeUserFromBoard(propertyId, user) {
      console.log("User:", user); // Sprawdźmy, co jest w obiekcie user
      
      await this.deleteUserFromBoard(propertyId, this.removeUserId);
    },
  },

  computed: {
    boardTotalLength() {
      return this.boards.length;
    }
  }
};
</script>

<style scoped src="../style/tables.css"></style>