import RestObject from './rest-object';
import Rest from './rest';

class Students extends RestObject {
  constructor({ id=null, ...rest }) {
    super();
    this.id = id;
    Object.assign(this, rest);
  }
  static async joinGroup(code) {
    const rest = new Rest();
    try {
      let response = await rest.patch(`${Students.URL}add-group/`, code)
      Object.assign(this, response.data);
      return this;
    } catch (err) {
      throw err.response.data;
    }
  }
  static async getGroup(params) {
    const rest = new Rest();
    try {
      let response = await rest.get(`${Students.URL}get-group/`, params)
      return response.data;
    } catch (err) {
      throw err.response.data;
    }
  }
  static async leaveGroup(params) {
    const rest = new Rest();
    try {
      let response = await rest.get(`${Students.URL}leave-group/`, params)
      Object.assign(this, response.data);
      return this;
    } catch (err) {
      throw err.response.data;
    }
  }
}

Students.URL = 'api//users/users/';

export default Students;