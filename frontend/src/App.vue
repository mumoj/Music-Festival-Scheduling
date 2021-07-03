<template>
  <div class="container-fluid">
    <home-page></home-page>
  </div>
</template>

<script>
import HomePage from './components/HomePage.vue'
import store from './store/index'

export default {
  name: 'App',
  store,
  components: {
    'homePage': HomePage,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
