import Vue from 'vue'
import Vuex from 'vuex'
import permission from './modules/permission'
import snackbar from './modules/snackbar'
import topics from './modules/topics'
import groups from './modules/groups'
import students from './modules/students'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    groups,
    topics,
    students,
    snackbar,
    permission
  }
})
