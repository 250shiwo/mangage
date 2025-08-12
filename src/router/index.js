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
      title:'家'
    },
    children:[
      {
        path:'/Hinfo',
        name:'Hinfo',
        component:()=>import('../views/Hinfo.vue'),
        meta: {
          title: '首页'
        },
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

router.beforeEach((to,from,next)=>{//beforeEach是router的钩子函数，在进入路由前执行
    if(to.meta.title){//判断是否有标题
        document.title = "学生请假管理系统"+" - "+ to.meta.title
    }
    next()  //执行进入路由，如果不写就不会进入目标页
})

export default router;
