import router from '@/router';
import State from './state';
import Http from './http';

const LOGIN_URL = 'api/login/';  // DODAJ 'api/'

class Auth {
  static async login(username, password) {
    const http = new Http();
    try {
      console.log('🔐 Wysyłam żądanie login do:', http.getConfig().baseURL + LOGIN_URL);
      console.log('📤 Dane logowania:', { username, password });
      
      const response = await http.fetch('post', LOGIN_URL, { username, password });
      
      console.log('✅ Odpowiedź z backendu:', response);
      console.log('🔑 Token:', response.data.token);
      
      State.setAccessToken(response.data.token);
      // DODANO: Zapisujemy username do localStorage
      State.setUsername(username);
      router.push({ name: 'Home' }).catch(() => {});
      return response;
    } catch (err) {
      console.log('❌ BŁĄD logowania:');
      console.log('Status:', err.response?.status);
      console.log('Dane błędu:', err.response?.data);
      console.log('Headers:', err.response?.headers);
      console.log('Cały error:', err);
      
      State.setAccessToken('');
      State.setRefreshToken('');
      State.setUserType(null);
      throw err;
    }
  }

  static async logout() {
    State.setAccessToken('');
    State.setPermissions(null);
    // DODANO: Czyścimy username przy wylogowaniu
    State.clearUsername();
    router.push({ name: 'Login' }).catch(() => {});
  }
}

export default Auth;
