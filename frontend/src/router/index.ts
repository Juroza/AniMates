import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView from '../views/HomeView.vue'
import TimeLineView from '../views/TimeLineView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/home', component: HomeView },
    {
      path: '/timeline',
      name: 'timeline', // Add this
      component: TimeLineView,
    },
  ],
})

export default router
