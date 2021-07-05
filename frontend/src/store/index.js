import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)
Vue.use(axios)

export default new Vuex.Store ({
  state: {
    loggingIn: false,
    loginError: null,
    loginSuccessful: false
  },
  mutations: {
    loginStart: state => state.loggingIn = true,
    loginStop: (state, errorMessage) => {
      state.loggingIn = false;
      state.loginError = errorMessage;
      state.loginSuccessful = !errorMessage;
    }
  },
  actions: {
    doLogin({ commit }, loginData) {
      commit('loginStart');

      axios.post('http://127.0.0.1:8000/accounts/login/', {
        ...loginData
      })
      .then((response) => {
        console.log(response)
        commit('loginStop', null)
      })
      .catch(error => {
        commit('loginStop', error.response.data.error)
      })
    }
  },
})
