import Vue from 'vue'
import Vuex from 'vuex'
import cookies from 'vue-cookies'
import Ciphers from '../assets/ciphers.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[0],
    token:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[1]||""
  },
  getters: {
  },
  mutations: {
    settonull(state){
      state.user="";
      state.token=""
    }
  },
  actions: {
  },
  modules: {
  }
})
