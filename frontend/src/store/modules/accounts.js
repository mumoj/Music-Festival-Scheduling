import axios from 'axios'

const state = {
    loggingIn: false,
    loginErrors: null,
    loginSuccessful: false
};

const mutations = {
	loginStart: state => state.loggingIn = true,
	loginStop: (state, errorMessages) => {
		state.loggingIn = false;
	    state.loginErrors = errorMessages;
	    state.loginSuccessful = !errorMessages;
	}
};

const actions = {
    doLogin({ commit }, loginData) {
    	commit('loginStart');

    	axios.post('accounts/login/', {...loginData})
    	.then(() => { commit('loginStop', null)
    	})
    	.catch(err => { 
	      	const errors = err.response.data
	        console.log(errors)
	        commit('loginStop', errors);
    	})

    }

};

const getters = {
	loggingIn: state => state.loggingIn,
	loginErrors: state => state.loginErrors,
	loginSuccessful:state => state.loginSuccessful
};

export default {
	state,
	getters,
 	mutations,
 	actions,
 }