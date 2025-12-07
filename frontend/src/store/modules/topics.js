import Topics from "../../service/topics";
import SelectOptions from '@/service/selectedOptions';



const state = {
  totalItems: 0,
  topicsChoices: [],
  topicsDetails: {},
  topicsList: [],
  errors: {},
  topicsListHeaders: [
    {
      text: 'Nazwa',
      value: 'name_topic',
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
  getTopics(state) {
    return state.topicsList;
  },
  getTopicsDetails(state) {
    return state.topicsDetails;
  },
  getTopicsCount(state) {
    return state.totalItems;
  },
  getTopicsErrors(state) {
    return state.errors;
  },
  getTopicsListHeaders(state) {
    return state.topicsListHeaders;
  },
  getTopicsItemsPerPage(state) {
    return state.itemsPerPage;
  },
  getTopicsChoices(state) {
    return state.topicsChoices;
  },
};

const mutations = {
  setTopics(state, payload) {
    state.totalItems = payload.count;
    state.topicsList = [ ...payload ];
  },
  setTopicsDetails(state, payload) {
    state.topicsDetails = { ...payload };
  },
  setTopicsErrors(state, payload) {
    state.errors = { ...payload };
  },
  setTopicsItemsPerPage(state, value) {
    state.itemsPerPage = value;
  },
  setTopicsDetailsProp(state, { prop, value }) {
    state.topicsDetails = { ...state.topicsDetails, [prop]: value };
    state.errors = { ...state.errors, [prop]: null };
  },
  setTopicsChoices(state, payload) {
    state.topicsChoices = [... payload];
    state.topicsNamesMap = { ...payload.reduce((acc, val) => (acc[val.id] = val.name, acc), {}) };
  },
};

const actions = {
  async fetchTopicsList(context, params) {
    try {
      context.commit('setTopics', await Topics.list(params));
      return true;
    } catch (error) {
      return false;
    }
  },
  async fetchTopicsDetails(context, id) {
    try {
      if (!id) {
        context.commit('setTopicsDetails', {});
        return;
      }
      context.commit('setTopicsDetails', await Topics.get(id));
      return true;
    } catch (error) {
      return false;
    }
  },
  async createTopics(context, topicsId) {
    const success_message = topicsId ? 'Temat został zaktualizowany.': 'Temat został utworzony.';
    try {
      const item = await new Topics(context.state.topicsDetails).save();
      context.commit('setTopicsDetails', item);
      context.commit('setTopicsErrors', {});
      context.commit('showMessage', { message: success_message });
      return true
    } catch (error) {
      context.commit('setTopicsErrors', error);
      return false
    }
  },
  async deleteTopics(context, payload) {
    try {
      await new Topics(payload).remove();
      return true;
    } catch (error) {
      return false;
    }
  },
  async fetchTopicsChoices(context, params=null) {
    try {
      context.commit('setTopicsChoices', await SelectOptions.get('topics', 'topics', params));
      return true
    } catch (error) {
      return false
    }
  },
};


export default {
  state,
  getters,
  mutations,
  actions
};