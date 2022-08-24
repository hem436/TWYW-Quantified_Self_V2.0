import Vue from 'vue'
import Vuex from 'vuex'
import cookies from 'vue-cookies'
import Ciphers from '../assets/ciphers.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_id:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[0]||"",
    user:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[1]||"",
    token:Ciphers.decode("Vigenere Cipher",cookies.get("user")||"",["Pwd"]).split(";")[2]||"",
    trackers:[]
  },
  getters:{
    tracker_types(state){
      return state.trackers.map(t=>t.tracker_type)
    },
    tracker_ids(state){
      return state.trackers.map(t=>t.tracker_id)
    },
    get_trackers(state){
      return state.trackers
    }
  },
  mutations: {
    logout(state){
      state.user="";
      state.token="";
      state.user_id="";
      state.trackers=[]
    },
    login(state,obj){
      state.user_id=obj.user_id;
      state.user=obj.username;
      state.token=obj.auth_token;
    },
    set_tracker(state,obj){
      state.trackers.push(obj)
    }
  },
  actions: {
  },
  modules: {
  }
})
