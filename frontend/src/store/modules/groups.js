import Groups from "../../service/groups";
import SelectOptions from '@/service/selectedOptions';

const state = {
  totalItems: 0,
  groupsChoices: [],
  groupsDetails: {},
  groupsList: [],
  groupsWithPreferences: [],
  errors: {},
  groupsListHeaders: [
    {
      text: 'Nazwa grupy',
      value: 'name_group',
    },
    {
      text: 'Prowadzący',
      value: 'lecturer_display.username',
    },
    {
      text: 'Temat',
      value: 'topic_display.name_topic',
    },
    {
      text: 'Kod',
      value: 'code',
    },
    {
      text: 'Akcje',
      value: 'actions',
      sortable: false
    }
  ],
  groupsWithPrefsHeaders: [
    {
      text: 'Nazwa grupy',
      value: 'name',
    },
    {
      text: 'Kod',
      value: 'code',
    },
    {
      text: 'Prowadzący',
      value: 'lecturer',
    },
    {
      text: 'Temat przypisany',
      value: 'assigned_topic.name',
    },
    {
      text: 'Liczba studentów',
      value: 'student_count',
    },
    {
      text: 'Preferencje (1, 2, 3)',
      value: 'preferences',
      sortable: false
    },
    {
      text: 'Studenci',
      value: 'students',
      sortable: false
    },
    {
      text: 'Akcje',
      value: 'actions',
      sortable: false
    }
  ],
  itemsPerPage: 5
};

const getters = {
  getGroups(state) {
    return state.groupsList;
  },
  getGroupsWithPreferences(state) {
    return state.groupsWithPreferences;
  },
  getGroupsDetails(state) {
    return state.groupsDetails;
  },
  getGroupsCount(state) {
    return state.totalItems;
  },
  getGroupsErrors(state) {
    return state.errors;
  },
  getGroupsListHeaders(state) {
    return state.groupsListHeaders;
  },
  getGroupsWithPrefsHeaders(state) {
    return state.groupsWithPrefsHeaders;
  },
  getGroupsItemsPerPage(state) {
    return state.itemsPerPage;
  },
  getGroupsChoices(state) {
    return state.groupsChoices;
  },
};

const mutations = {
  setGroups(state, payload) {
    state.totalItems = payload.count;
    state.groupsList = [ ...payload ];
  },
  setGroupsWithPreferences(state, payload) {
    state.groupsWithPreferences = [ ...payload ];
    state.totalItems = payload.length;
  },
  setGroupsDetails(state, payload) {
    state.groupsDetails = { ...payload };
  },
  setGroupsErrors(state, payload) {
    state.errors = { ...payload };
  },
  setGroupsItemsPerPage(state, value) {
    state.itemsPerPage = value;
  },
  setGroupsDetailsProp(state, { prop, value }) {
    state.groupsDetails = { ...state.groupsDetails, [prop]: value };
    state.errors = { ...state.errors, [prop]: null };
  },
  setGroupsChoices(state, payload) {
    state.groupsChoices = [... payload];
    state.groupsNamesMap = { ...payload.reduce((acc, val) => (acc[val.id] = val.name, acc), {}) };
  },
};

const actions = {
  async fetchGroupsList(context, params) {
    try {
      context.commit('setGroups', await Groups.list(params));
      return true;
    } catch (error) {
      return false;
    }
  },
  
  async fetchGroupsWithPreferences(context, params) {
    try {
      const data = await Groups.listWithPreferences(params);
      context.commit('setGroupsWithPreferences', data);
      return true;
    } catch (error) {
      console.error('Błąd pobierania grup z preferencjami:', error);
      return false;
    }
  },
  
  async fetchGroupsDetails(context, id) {
    try {
      if (!id) {
        context.commit('setGroupsDetails', {});
        return;
      }
      context.commit('setGroupsDetails', await Groups.get(id));
      return true;
    } catch (error) {
      return false;
    }
  },
  async createGroups(context,groupsId) {
    const success_message = groupsId ? 'Grupa zostala zaktualizowana.': 'Grupa zostala utworzona.';
    try {
      const item = await new Groups(context.state.groupsDetails).save();
      context.commit('setGroupsDetails', item);
      context.commit('setGroupsErrors', {});
      context.commit('showMessage', { message: success_message });
      return true
    } catch (error) {
      context.commit('setGroupsErrors', error);
      return false
    }
  },
  async deleteGroups(context, payload) {
    try {
      await new Groups(payload).remove();
      return true;
    } catch (error) {
      return false;
    }
  },
  async fetchGroupsChoices(context, params=null) {
    try {
      context.commit('setGroupsChoices', await SelectOptions.get('students', 'groups', params));
      return true
    } catch (error) {
      return false
    }
  },
  async fetchGroupsDetailsForUser(context) {
    try {
      console.log('blagam')
      context.commit('setGroupsDetails', await Groups.getGroup());
      return true;
    } catch (error) {
      return false;
    }
  },
};

export default {
  state,
  getters,
  mutations,
  actions
};
