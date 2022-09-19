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
import Ciphers from './scripts/ciphers.js'
import * as echarts from './scripts/echarts.js'

Vue.use(VueCookies);
Vue.prototype.$echarts= echarts;
Vue.prototype.$Ciphers = Ciphers;
Vue.filter("date_format", function(value) {
  let currentdate = new Date(value);
  let mstr = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
  ];
  let datetime =
    currentdate.getDate() +
    "/" +
    mstr[currentdate.getMonth()] +
    "/" +
    currentdate.getFullYear() +
    ", " +
    currentdate.getHours() +
    ":" +
    currentdate.getMinutes() +
    ":" +
    currentdate.getSeconds() +
    "." +
    currentdate.getMilliseconds();
  // if(!value) return ''
  // value = value.toString()
  return datetime;
});

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
