import RestObject from './rest-object';
import Rest from './rest';
class Groups extends RestObject {
  constructor({ id, ...rest }) {
    super();
    this.id = id;
    Object.assign(this, rest);
  }
  
  static async getGroup(params) {
    const rest = new Rest();
    try {
      let response = await rest.get(`${Groups.URL}get-group/`, params)
      return response.data;
    } catch (err) {
      throw err.response.data;
    }
  }
  
  // NOWA METODA: Lista grup z preferencjami (dla wykładowców)
  static async listWithPreferences(params = {}) {
    const rest = new Rest();
    try {
      const response = await rest.get(`${Groups.URL}all-with-preferences/`, params);
      return response.data;
    } catch (err) {
      throw err.response.data;
    }
  }
}

Groups.URL = 'api/groups/groups/';
export default Groups;
