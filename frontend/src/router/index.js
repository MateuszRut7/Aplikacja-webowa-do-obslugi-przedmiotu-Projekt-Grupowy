import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import TopicsTable from '../views/TopicsTable.vue'
import TopicsForm from  '../views/TopicsForm.vue'
import TopicsDetails from  '../views/TopicsDetails.vue'
import GroupsTable from '../views/GroupsTable.vue'
import Groups from  '../views/Groups.vue'
import GroupsForm from  '../views/GroupsForm.vue'
import GroupsFormForTable from  '../views/GroupsFormForTable.vue'
import State from '@/service/state';

Vue.use(VueRouter);
const checkIfAuthorized = (to, from, next) => { (!State.isAuth() || (!! to.meta.requiredPerm && ! State.getPermissions().includes(to.meta.requiredPerm))) ? next('/login') : next(); };
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/topicsTable',
    name: 'TopicsTable',
    component: TopicsTable,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/topicsForm/:id?',
    name: 'TopicsForm',
    component: TopicsForm,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/topicsDetails/:id?',
    name: 'TopicsDetails',
    component: TopicsDetails,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/groupsTable',
    name: 'GroupsTable',
    component: GroupsTable,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/Groups/',
    name: 'Groups',
    component: Groups,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/groupsForm/:id?',
    name: 'GroupsForm',
    component: GroupsForm,
    beforeEnter: checkIfAuthorized,
  },
  {
    path: '/groupsFormForTable/:id?',
    name: 'GroupsFormForTable',
    component: GroupsFormForTable,
    beforeEnter: checkIfAuthorized,
  },
 
]

const router = new VueRouter({
  routes
})

export default router
