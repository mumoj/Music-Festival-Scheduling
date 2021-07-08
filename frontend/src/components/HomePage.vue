<template>
    <div class="container">
        <h1> The Kenya Music Festival </h1>
        <login></login> 
    </div>
</template>

<script>
    import Login from './auth/Login.vue'

    export default {
        name:'HomePage',
        components: {
            'Login': Login
        }
    }
</script>