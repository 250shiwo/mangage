import Vue from 'vue'
import Vuex from 'vuex'
import router,{resetRouter}from '@/router'

Vue.use(Vuex)

function addNewRoute(menuList) {
  const routes = router.options.routes;
  const menuMap = {};
  
  // 构建菜单映射表
  menuList.forEach(menu => {
    menuMap[menu.menuCode] = menu;
  });

  routes.forEach(routeItem => {
    if (routeItem.path === '/Home') {
      menuList.forEach(menu => {
        if (menu.menuParentCode) {
          const parentMenu = menuMap[menu.menuParentCode];
          if (parentMenu) {
            const childRoute = {
              path: `/${parentMenu.menuClick}/${menu.menuClick}`,
              name: menu.menuname,
              meta: {
                title: menu.menuname,
              },
              component: () => import('../views/' + menu.menuComponent)
            };
            routeItem.children.push(childRoute);
          }
        } else {
          const childRoute = {
            path: `/${menu.menuClick}`,
            name: menu.menuname,
            meta: {
              title: menu.menuname,
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

      addNewRoute(menuList)
    }
  },
  actions: {
  },
  modules: {
  }
})
