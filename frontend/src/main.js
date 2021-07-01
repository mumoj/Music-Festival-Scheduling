import Vue from 'vue'
import { createApp } from 'vue'

import App from './App.vue'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import store from './store'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)


createApp(App).use(store).mount('#app')
