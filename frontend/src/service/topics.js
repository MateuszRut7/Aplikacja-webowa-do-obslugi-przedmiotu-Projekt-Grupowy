import RestObject from './rest-object';

class Topics extends RestObject {
  constructor({ id, ...rest }) {
    super();
    this.id = id;
    Object.assign(this, rest);
  }
}

Topics.URL = 'api/topics/topics/';  // DODAJ 'api/'

export default Topics;