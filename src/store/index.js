import Vue from 'vue'
import Vuex from 'vuex'
import router,{resetRouter}from '@/router'

Vue.use(Vuex)

function addNewRoute(menuList) {
  let routes = router.options.routes
  routes.forEach(routeItem=>{
    if(routeItem.path=='/Home'){
      menuList.forEach(menu=>{
        let childRoute = {
          path:'/'+menu.menuClick,
          name:menu.menuname,
          meta:{
            title:'menu.menuname',
          },
          component:()=>import('../views/' + menu.menuComponent)
        }
        routeItem.children.push(childRoute)
      })
    }
  })
  resetRouter()
  router.addRoutes(routes)
}

export default new Vuex.Store({
  state: {
    menu:[]
  },
  getters: {
    getMenu(state){
      return state.menu
    }
  },
  mutations: {
    setMenu(state,menuList){
      state.menu = menuList

      addNewRoute(menuList)
    }
  },
  actions: {
  },
  modules: {
  }
})
