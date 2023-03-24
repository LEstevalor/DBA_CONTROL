import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'HelloWorld',
    //   component: HelloWorld
    // }
    {
      path: '/', // 公有模板页
      name: 'index',
      component: () => import('../components/index.vue'),
      children: [
        {
          path: '/top', // 要跟在父路径的路径后，/father/child
          name: 'index.top', // 名称也是
          component: () => import('../components/top.vue')
        },
        {
          path: '/college',
          name: 'index.college',
          component: () => import('../components/college.vue')
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/login.vue')
      // component: login
    }
  ]
})
