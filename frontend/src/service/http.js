import axios from 'axios';
import Qs from 'qs';

axios.defaults.paramsSerializer = params => Qs.stringify(params, { arrayFormat: 'repeat' });

class Http {
  constructor() {
    this.http = axios.create(this.getConfig());
  }

  fetch(method, url, params) {
    return this.http[method](url, params);
  }

  getConfig() {
    return {
      headers: {
        'Content-Type': 'application/json'
      },
      // USUŃ baseURL - niech proxy działa
      // baseURL: 'http://localhost:8000/api/',
    };
  }
}

export default Http;