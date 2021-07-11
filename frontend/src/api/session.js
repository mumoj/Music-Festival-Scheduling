import axios from 'axios';

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

const session = axios.create({
	baseURL: `http://127.0.0.1:8000/`,
	headers: {
    	Accept: "application/json",
    	"Content-type": "application/json"
    },

  	timeout: 10000,
  	withCredentials: true, 

	xsrfCookieName: CSRF_COOKIE_NAME,
	xsrfHeaderName: CSRF_HEADER_NAME,

});

export default session;
