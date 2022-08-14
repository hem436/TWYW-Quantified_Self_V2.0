import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },{
      path: '/dashboard',
      component: ()=>import('@/components/dash/DashIndex'),
      children: [
      {
        path: '/',
        name: 'dash.home',
        component: () => import('@/components/dash/DashHome'),
        meta: {
          title: 'Home Dashboard',
        }
      }]
    },
    {
      path: '/login',
      name: 'Login',
      component: ()=>import('@/components/LogIn')
    },
    {
      path: '/signup',
      name: 'signup',
      component: ()=>import('@/components/SignUp')
    }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
