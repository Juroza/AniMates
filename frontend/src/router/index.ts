import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView from '../views/HomeView.vue'
import TimeLineView from '../views/TimeLineView.vue'
import CanvasView from '../views/CanvasView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/home', component: HomeView },
    {
      path: '/timeline',
      name: 'timeline',
      component: TimeLineView,
    },
    {
      path: '/canvas',
      name: 'canvas',
      component: CanvasView,
    },
  ],
})

export default router
