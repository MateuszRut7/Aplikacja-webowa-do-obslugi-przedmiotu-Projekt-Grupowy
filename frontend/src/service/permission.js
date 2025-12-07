import RestObject from './rest-object';
import Rest from './rest';

class Permissions extends RestObject {
  constructor({ id, ...rest }) {
    super();
    this.id = id;
    Object.assign(this, rest);
  }

  static async getPermissions() {
    const rest = new Rest();
    try {
      const response = await rest.get(`${this.URL}`);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  }
}

Permissions.URL = 'api/permissions/';  // Z 'permissions/' na 'api/permissions/'
export default Permissions;