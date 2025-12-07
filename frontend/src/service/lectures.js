import RestObject from './rest-object';

class Lectures extends RestObject {
  constructor({ id, ...rest }) {
    super();
    this.id = id;
    Object.assign(this, rest);
  }
}

Lectures.URL = 'api/lectures/lectures/';

export default Lectures;