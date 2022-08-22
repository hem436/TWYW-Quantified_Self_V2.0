import Vue from 'vue'
import Vuex from 'vuex'
import cookies from 'vue-cookies'
import Ciphers from '../assets/ciphers.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_id:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[0]||"",
    user:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[1]||"",
    token:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[2]||""
  },
  getters: {
  },
  mutations: {
    logout(state){
      state.user="";
      state.token="";
      state.user_id="";
    },
    login(state,obj){
      state.user_id=obj.user_id;
      state.user=obj.username;
      state.token=obj.auth_token;
    }
  },
  actions: {
  },
  modules: {
  }
})
