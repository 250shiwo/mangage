import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
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
    meta:{
      title:'首页'
    },
    children:[
      {
        path:'/Hinfo',
        name:'Hinfo',
        component:()=>import('../views/Hinfo.vue')
      },
    ]
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
