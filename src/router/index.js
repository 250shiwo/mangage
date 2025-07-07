import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import AboutView from '../views/AboutView.vue'
import StudentView from '../views/Student.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/Home',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/About',
    name: 'About',
    component: AboutView
  },
  {
    path: '/Student',
    name: 'Student',
    component: StudentView
  },
]

const router = new VueRouter({
  routes
})

export default router
