import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/accounts/auth'


Vue.use(Vuex)


export default new Vuex.Store ({
    namespaced: true,
    modules : {
        auth,
    }
})
