const AUTO_LOGOUT_TIME = process.env.VUE_AUTO_LOGOUT_TIME ? parseInt(process.env.VUE_AUTO_LOGOUT_TIME): 15 * 60;


class State {
  static setAccessToken(token) {
    localStorage.setItem('authTimeStamp', token ? Date.now().toString() : '0');
    localStorage.setItem('access-token', token);
  }

  static getAccessToken() {
    return localStorage.getItem('access-token');
  }

  static setUserType(userType) {
    localStorage.setItem('user-type', userType);
  }

  static authTimeStamp() {
    return parseInt(localStorage.getItem('authTimeStamp') || '0');
  }

  static loginTimeDelta() {
    return (Date.now() - this.authTimeStamp());
  }

  static isAuth() {
    return this.loginTimeDelta() / 100000 <= AUTO_LOGOUT_TIME;
  }

  static idleCountdown() {
    return this.isAuth() ? AUTO_LOGOUT_TIME - this.loginTimeDelta() / 100000 : 0;
  }

  static setPermissions(permissions) {
    localStorage.setItem('permissions', permissions);
  }

  static getPermissions() {
    return localStorage.getItem('permissions');
  }

  static getUserType() {
    return localStorage.getItem('user-type');
  }

  static isUser() {
    return localStorage.getItem('user-type') === 'user';
  }

  // DODANE METODY DO OBSŁUGI USERNAME
  static setUsername(username) {
    localStorage.setItem('username', username);
  }

  static getUsername() {
    return localStorage.getItem('username');
  }

  static clearUsername() {
    localStorage.removeItem('username');
  }
}

export default State;
