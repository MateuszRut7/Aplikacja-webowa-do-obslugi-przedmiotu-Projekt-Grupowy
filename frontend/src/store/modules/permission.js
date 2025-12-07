import Permissions from "../../service/permission";

const state = {
  permission: {},
  linksPermissions: [],
  links: [
    { icon: 'mdi-home', text: 'Strona główna', route: '/' },
    { icon: 'mdi-table', text: 'Lista tematów', route: '/topics' },
    { icon: 'mdi-table', text: 'Lista tematów 2', route: '/topicsTable', requiredPerm: 'lecturer', canView: 1},
    { icon: 'mdi-account-edit', text: 'Grupy', route:'/groupsTable', requiredPerm: 'lecturer'},
    { icon: 'mdi-account-edit', text: 'Studenci', route: '/studentsTable', requiredPerm: 'lecturer'}, 
    { icon: 'mdi-account-group', text: 'Twoja grupa', route: '/groups' },
  ]
};

const mutations = {
  setPermissions(state, payload) {
    state.permission = payload;
  },
  setLinksPermissions(state, payload) {
    state.linksPermissions = payload
  }
};

const getters = {
  getPermissions(state) {
    return state.permission;
  },
  getLinksPermissions(state) {
    return state.linksPermissions
  }
};

const actions = {
  async updatePermissions(context) {
    try {
      const perms = await Permissions.getPermissions();
      context.commit('setPermissions', perms);
      return perms;
    } catch(error) {
      console.log('Błąd pobierania permissions, używam fallback');
      const fallbackPerms = ['student']; // Domyślnie każdy jest studentem
      context.commit('setPermissions', fallbackPerms);
      return fallbackPerms;
    }
  },

  async updateLinks(context, perms) {
    const table = []
    for (const i in state.links){
      const link = state.links[i];
      // Jeśli link nie wymaga permisji lub użytkownik ma wymaganą permisję
      if (!link.requiredPerm || perms.includes(link.requiredPerm)) {
        table.push(link)
      }
    }
    context.commit('setLinksPermissions', table);
  }
};``

export default {
  state,
  getters,
  mutations,
  actions
};