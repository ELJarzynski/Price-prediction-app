import { createRouter, createWebHistory } from 'vue-router';
import home from '../views/home.vue'; 
import LogIn from '../views/LogIn.vue'; 
import SignUp from '../views/SignUp.vue'; 
import Tables from '../views/Tables.vue'; 
import RealEstatePrice from '../views/RealEstatePrice.vue'; 
const routes = [
  {
    path: '/',
    name: 'home',
    component: home
  },
  {
    path: '/log-in',
    name: 'login',
    component: LogIn
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/price',
    name: 'price',
    component: RealEstatePrice
  },
  {
    path: '/tables',
    name: 'tables',
    component: Tables
  },

];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;