import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import AboutView from '../views/AboutView.vue'
import StudentView from '../views/StudentView.vue'
import Student from '@/views/UserManage/Student.vue'
import Hinfo from '@/views/Hinfo.vue'
Vue.use(VueRouter)
Vue.component('Student',Student)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/Home',
    name: 'Home',
    component: HomeView,
    children:[
      {
        path:'/Hinfo',
        name:'Hinfo',
        meta:{
          title:'首页'
        },
        component:Hinfo
      }
    ]
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
