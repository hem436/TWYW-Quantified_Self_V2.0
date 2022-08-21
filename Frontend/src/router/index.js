import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index.js'

Vue.use(VueRouter)

const routes = [{
    path: '/dashboard',
    component: () => import('@/views/DashIndex'),
    children: [{
        path: '/',
        name: 'dash.home',
        component: () => import('@/components/DashHome'),
        meta: {
          title: 'Home Dashboard',
          auth:true
        }
      },
      {
        path: 'tracker/:id',
        name: 'dash.tracker',
        component: () => import('@/components/DashTracker')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LogIn'),
    meta:{auth:false}
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('@/views/SignUp'),
    meta:{auth:false}
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(async(to, from,next) => {
  // instead of having to check every route record with "WyI1MjJlMDBmMGI3ODE0NTg0YjcwMmEyN2IwZGEwOTFkYiJd.Yv3haw.CCf1H1tUJqdwZmusxwOFuCCLwkI"
  // to.matched.some(record => record.meta.requiresAuth)
  console.log(from.path+'-->'+to.path)
  console.log(store.state.token.length)
  if (to.meta.auth) {
    if(store.state.token.length==83)
    {next()}
    else{next({name:'login'})}
  }
  else {
  next()}
})
export default router
