import auth from '../../../api/accounts';
import session from '../../../api/session';


const TOKEN_STORAGE_KEY = 'TOKEN_STORAGE_KEY';
const isProduction = process.env.NODE_ENV === 'production';

const initialState = {
    authenticating: false,
    loginErrors: null,
    token: null,
};

const getters = {
    isAuthenticated: state => !!state.token,
};

const mutations = {
    'LOGIN_BEGIN'(state) {
        state.authenticating = true;
    },

    'LOGIN_STOP'(state, errorMessages) {
        state.authenticating = false;
        state.loginErrors = errorMessages;
    },

    'LOGOUT'(state) {
        state.authenticating = false;
    },

    'SET_TOKEN'(state, token) {
        if (!isProduction) localStorage.setItem(TOKEN_STORAGE_KEY, token);
        session.defaults.headers.Authorization = `Token ${token}`;
        state.token = token;
    },

    'REMOVE_TOKEN'(state) {
        localStorage.removeItem(TOKEN_STORAGE_KEY);
        delete session.defaults.headers.Authorization;
        state.token = null;
    },
};

const actions = {
    doLogin({ commit }, { email, password }) {
        commit('LOGIN_BEGIN');
        return auth.login(email, password)
            .then((data) => {
                commit('LOGIN_STOP', null);
                commit('SET_TOKEN', data.key);
            })
            .catch((err) => {
                let errorMessages = err.response.data;
                commit('LOGIN_STOP', errorMessages );
            })
    },

    doLogout({ commit }) {
        return auth.logout()
            .then(() => commit('LOGOUT'))
            .finally(() => commit('REMOVE_TOKEN'));
    },

    initialize({ commit }) {
        const token = localStorage.getItem('TOKEN_STORAGE_KEY');
        if (isProduction && token) {
            commit('REMOVE_TOKEN');
        }
        if (!isProduction && token) {
            commit('SET_TOKEN', token);
        }
    },
};

export default {
    namespaced: true,
    state: initialState,
    getters,
    mutations,
    actions,
};

