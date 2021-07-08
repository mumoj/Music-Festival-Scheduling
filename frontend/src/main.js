import Vue from 'vue'
import App from './App.vue'
import store from './store'

import axios from 'axios'
import vuetify from './plugins/vuetify'


Vue.config.productionTip = false
axios.defaults.baseURL = 'http://127.0.0.1:8000/'

new Vue({
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')
 

