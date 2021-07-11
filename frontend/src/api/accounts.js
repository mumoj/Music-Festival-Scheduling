import session from './session';

export default {
	login(email, password) {
		return session.post('/accounts/login/', {email, password });
	},
	logout() {
		return session.post('/accounts/logout/', {});
	},
	createAccount(email, password1, password2) {
		return session.post('accounts/register/', { email, password1, password2 });
	},
	changeAccountPassword(password1, password2) {
		return session.post('/accounts/password-reset/', { password1, password2 });
	},
	resetAccountPasswordConfirmation(uid, token, new_password1, new_password2) { // eslint-disable-line camelcase
	return session.post('/accounts/password-reset-confirm/', { uid, token, new_password1, new_password2 });
	},
	verifyAccountEmail(key) {
	return session.post('/accounts/verify-email/', { key });
	},
};