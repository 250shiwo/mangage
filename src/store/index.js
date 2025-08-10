import Vue from 'vue'
import Vuex from 'vuex'
import router,{resetRouter}from '@/router'
import createPersistedState from 'vuex-persistedstate'
Vue.use(Vuex)

function addNewRoute(menuList) {
  let routes = router.options.routes;

  const menuMap = {};
  
  // 构建菜单映射表
  menuList.forEach(menu => {
    menuMap[menu.menuCode] = menu;
  });

  routes.forEach(routeItem => {
    if (routeItem.path === '/Home') {
      menuList.forEach(menu => {
        if (menu.menuParentCode) {
          let parentMenu = menuMap[menu.menuParentCode];
          if (parentMenu) {
            let childRoute = {
              path: `/${parentMenu.menuClick}/${menu.menuClick}`,
              name: menu.menuName,
              meta: {
                title: menu.menuName,
              },
              component: () => import('../views/' + menu.menuComponent)
            };
            routeItem.children.push(childRoute);
          }
        } else {
          let childRoute = {
            path: `/${menu.menuClick}`,
            name: menu.menuName,
            meta: {
              title: menu.menuName,
            },
            component: () => import('../views/' + menu.menuComponent)
          };
          routeItem.children.push(childRoute);
        }
      });
    }
  });
  resetRouter();
  router.addRoutes(routes);
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
      //添加路由
      addNewRoute(menuList)
    },
    setRouter(state,menuList){
      addNewRoute(menuList)
    }
  },
  plugins:[createPersistedState()]
})
