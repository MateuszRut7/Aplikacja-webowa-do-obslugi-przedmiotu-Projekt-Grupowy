

import Http from './http';
import State from './state';
import store from '@/store';

const CSRF_HEADER_NAME = 'X-CSRFTOKEN';
const CSRF_COOKIE_NAME = 'csrftoken';

class AuthHttp extends Http {
  constructor() {
    super();
    this.http.interceptors.response.use(response => response, this.$handleError.bind(this));
  }

  $handleError(error) {
    let msg = [];

    function flatten(target, opts) {
      opts = opts || {};

      let delimiter = opts.delimiter || '.';

      function step(object, prev) {
        Object.keys(object).forEach(function(key) {
          let value = object[key];
          let isArray = Array.isArray(value);
          let type = Object.prototype.toString.call(value);
          let isObject = type === '[object Object]';

          let newKey = prev
            ? prev + delimiter + key
            : key;

          if (!isArray && isObject && Object.keys(value).length) {
            return step(value, newKey);
          }

          if (isArray) {
            Array.prototype.push.apply(msg, value);
          } else {
            msg.push(value);
          }
        });
      }

      step(target);
    }
    if (!(error.response === 'undefinied' && error.response.data ==='undefinied')) {
      if (error.response.status === 400 || error.response.status === 404 || error.response.status === 403) {
        flatten(error.response.data);
      } else if (error.response.status === 401) {
        msg.push('Nie masz uprawnień do danej czynności');
      }
    }

    if (!msg.length) {
      msg.push('Wystąpił nieoczekiwany błąd.');
    }

    store.commit('showMessage', { message: msg.join('\n'), color: 'error' });

    throw error;
  }

  getConfig() {
    return {
      withCredentials: true,
      xsrfHeaderName: CSRF_HEADER_NAME,
      xsrfCookieName: CSRF_COOKIE_NAME,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${State.getAccessToken()}`
      },
      // USUŃ baseURL tutaj też
      // baseURL: 'http://localhost:8000/api/',
    };
  }
}

export default AuthHttp;
