// npm install vue-cookies --save
//
// // require
// var Vue = require('vue')
// Vue.use(require('vue-cookies'))

import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import VueCookies from 'vue-cookies'
import Ciphers from './assets/ciphers.js'


Vue.use(VueCookies);
Vue.prototype.$Ciphers = Ciphers;

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
