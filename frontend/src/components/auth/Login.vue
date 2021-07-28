<template>
    <div class="login">

        <v-form @submit.prevent="loginSubmit">
            <v-container>
                <p v-if="isAunthenticated"> Login Successful </p>
                <div v-else-if="nonFieldErrors">
                    <div v-for="error,index in nonFieldErrors" :key="index">
                        {{ error }}
                    </div>
                </div>
                <v-row>
                    <v-col col="6" sm="12" xs="12" md="6">
                        <v-text-field
                            v-model="email.value"
                            label="@"
                            type="email"
                            :error-messages = "email.error"
                            required></v-text-field>
                    </v-col>
                    <v-col col="6" sm="12" xs="12" md="6">
                        <v-text-field
                            v-model="password.value"
                            label="Password"
                            type="password"
                            :error-messages = "password.error"
                            required></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <button type="submit">Login</button>
                </v-row>
            </v-container>
        </v-form>
    </div>    
</template>

<script>
    import { mapGetters, mapActions } from 'vuex';

    export default {
        name: 'Login',
        data() {
            return {
                email: {
                    value: '',
                    error: null
                },
                password: {
                    value:'',
                    error:null
                },
                nonFieldErrors: null
            }
        },
        computed: {
            ...mapGetters({
                authenticating: 'auth/authenticating',
                loginErrors: 'auth/loginErrors',
            }),
            isAunthenticated () {
                return this.$store.getters['auth/isAunthenticated']
            },
        },
        methods: {
            ...mapActions({
                doLogin: 'auth/doLogin'
            }),
            loginSubmit() {
                this.doLogin({
                    email: this.email.value,
                    password: this.password.value
                })
            },
            
        },
        watch: {
            loginErrors : {
                handler(val){
                    if (val.non_field_errors){
                        this.nonFieldErrors = val.non_field_errors
                    }else if (val.email){
                        this.email.error = val.email
                    }else {
                        this.password.errors = val.password
                    }
                },
                deep: true,
            }
        }
    }
</script>

<style scoped lang="scss">
  
    
</style>


