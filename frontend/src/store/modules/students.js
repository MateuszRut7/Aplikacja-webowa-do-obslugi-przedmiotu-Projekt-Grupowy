import Students from "../../service/students";
import SelectOptions from '@/service/selectedOptions';



const state = {
  totalItems: 0,
  hasGroup: null,
  studentsList: [],
  studentsChoices: [],
  studentsNameMap: {},
  studentsDetails: {},
  errors: {},
  selectedStudents: {},
  studentsListHeaders: [
    {
      text: 'Imię',
      value: 'first_name'
    },
    {
      text: 'Nazwisko',
      value: 'last_name'
    },
    {
      text: 'Numer indeksu',
      value: 'numer_index'
    },
  ],
  itemsPerPage: 5
};

const getters = {
  getStudents(state) {
    return state.studentsList;
  },
  getStudentsDetails(state) {
    return state.studentsDetails;
  },
  getStudentsCount(state) {
    return state.totalItems;
  },
  getStudentsErrors(state) {
    return state.errors;
  },
  getStudentsListHeaders(state) {
    return state.studentsListHeaders;
  },
  getStudentsItemsPerPage(state) {
    return state.itemsPerPage;
  },
  getStudentsChoices(state) {
    return state.studentsChoices;
  },
  getSelectedStudents(state) {
    return state.selectedStudents;
  },
  getHasGroup(state) {
    return state.hasGroup;
  }
};

const mutations = {
  setStudents(state, payload) {
    state.totalItems = payload.count;
    state.studentsList = [ ...payload ];
  },
  setStudentsDetails(state, payload) {
    state.studentsDetails = { ...payload };
  },
  seStudentsErrors(state, payload) {
    state.errors = { ...payload };
  },
  setStudentsItemsPerPage(state, value) {
    state.itemsPerPage = value;
  },
  setStudentsDetailsProp(state, { prop, value }) {
    state.studentsDetails = { ...state.studentsDetails, [prop]: value };
    state.errors = { ...state.errors, [prop]: null };
  },
  setStudentsChoices(state, payload) {
    state.studentsChoices = [... payload];
    state.studentsNamesMap = { ...payload.reduce((acc, val) => (acc[val.id] = val.name, acc), {}) };
  },
  setSelectedStudent(state, value) {
    state.selectedStudent = { ...value };
  },
  setHasGroup(state, value) {
    state.hasGroup = value;
  }
};

const actions = {
  async fetchStudentsList(context, params) {
    try {
      context.commit('setStudents', await Students.list(params));
      return true;
    } catch (error) {
      return false;
    }
  },
  async fetchStudentsDetails(context, id) {
    try {
      if (!id) {
        context.commit('setStudentsDetails', {});
        return;
      }
      let student = await Students.get(id)
      context.commit('setStudentsDetails', student);
      return student;
    } catch (error) {
      return false;
    }
  },
  async createStudents(context, studentsId) {
    const success_message = studentsId ? 'Temat został zaktualizowany.': 'Temat został utworzony.';
    try {
      const item = await new Students(context.state.studentsDetails).save();
      context.commit('setStudentsDetails', item);
      context.commit('setStudentsErrors', {});
      context.commit('showMessage', { message: success_message });
      return true
    } catch (error) {
      context.commit('setStudentsErrors', error);
      return false
    }
  },
  async deleteStudents(context, payload) {
    try {
      await new Students(payload).remove();
      return true;
    } catch (error) {
      return false;
    }
  },
  async fetchStudentsChoices(context, params=null) {
    try {
      context.commit('setStudentsChoices', await SelectOptions.get('students', 'student', params));
      return true;
    } catch (error) {
      return false;
    }
  },
  async joinGroup(context, code) {
    try {
      if (code === null) {
        context.commit('showMessage', { message: 'Proszę podać kod', color: 'error' });
        return false;
      }
      await Students.joinGroup(code)
      context.commit('showMessage', { message: 'Zostałeś dodany do grupy' });
      return true;
    } catch (error) {
      return false
    }
  },
  async fetchUserGroup(context) {
    try {
      let data = await Students.getGroup();
      context.commit('setHasGroup', data);
      return true;
    } catch (error) {
      return false;
    }
  },
  async leaveGroup() {
    try {
      await Students.leaveGroup();
      return true;
    } catch(error) {
      return false;
    }
}
}


export default {
  state,
  getters,
  mutations,
  actions
};