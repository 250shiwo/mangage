import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import AboutView from '../views/AboutView.vue'
import StudentView from '../views/StudentView.vue'
import Student from '@/views/UserManage/Student.vue'
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
    component: HomeView,
    children:[
      {
        path:'/Hinfo',
        name:'Hinfo',
        meta:{
          title:'首页'
        },
        component:()=>import('../views/Hinfo.vue')
      },
      // {
      //   path: '/User',
      //   name: 'User',
      //   meta: {
      //     title: '用户管理'
      //   },
      //   component: () => import('../views/UserManage/Student.vue')
      // },
      // {
      //   path: '/CollegeMajor',
      //   name: 'CollegeMajor',
      //   meta: {
      //     title: '学院专业管理'
      //   },
      //   component: () => import('../views/SchoolManage/Major.vue')
      // }
    ]
  },
  {
    path: '/About',
    name: 'About',
    component: AboutView
  },
]
export function resetRouter(){
  router.matcher = new VueRouter({
    mode:'history',
    routes:[]
  }).matcher
}


const router = new VueRouter({
  mode:'history',
  routes
})

export default router
