import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/dashboard',
      component: ()=>import('@/components/dash/DashIndex'),
      children: [
      {
        path: '/',
        name: 'dash.home',
        component: () => import('@/components/dash/Home'),
        meta: {
          title: 'Home Dashboard',
        }
      }]
    },
    {
      path: '/login',
      name: 'Login',
      component: ()=>import('@/components/Login')
    },
    {
      path: '/signup',
      name: 'signup',
      component: ()=>import('@/components/Signup')
    }
  ]
})
