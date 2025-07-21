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

const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(to) {
  return VueRouterPush.call(this, to).catch(err => err)
}

export default router;
