import RestObject from './rest-object';
import Rest from './rest';


class SelectOptions extends RestObject {

  constructor({ id='', name='', ...rest }) {
    super();
    this.id = id;
    this.name = name;
    Object.assign(this, rest);
  }

  static async get(module, object, params) {
    const rest = new Rest();
    try {
      let response = await rest.get(`${module}/${object}/choices/`, params);
      return response.data.map(select_option => new SelectOptions(select_option));
    } catch (err) {
      return [];
    }
  }
  static async get_static(module, object, fieldNames, params = {}) {
    const rest = new Rest();
    params.field_name = fieldNames;
    try {
      let response = await rest.get(`${module}/${object}/static-choices/`, params);
      return response.data;
    } catch (err) {
      return [];
    }
  }
}

export default SelectOptions;
