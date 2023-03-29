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
        },
        {
          path: '/major',
          name: 'index.major',
          component: () => import('../components/major.vue')
        },
        {
          path: '/teacher',
          name: 'index.teacher',
          component: () => import('../components/teacher.vue')
        },
        {
          path: '/student',
          name: 'index.student',
          component: () => import('../components/student.vue')
        },
        {
          path: '/grade',
          name: 'index.grade',
          component: () => import('../components/grade.vue')
        },
        {
          path: '/course',
          name: 'index.course',
          component: () => import('../components/course.vue')
        },
        {
          path: '/teach_student_class',
          name: 'index.teach_student_class',
          component: () => import('../components/teach_student_class.vue')
        },
        {
          path: '/user',
          name: 'index.user',
          component: () => import('../components/user.vue')
        },
        {
          path: '/setting',
          name: 'index.setting',
          component: () => import('../components/setting.vue')
        },
        {
          path: '/logs',
          name: 'index.logs',
          component: () => import('../components/log.vue')
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
