<template>
  <nav>

     <v-toolbar flatt app class="indigo accent-4" >
            <v-app-bar-nav-icon 
                color="white"
                @click="drawer =!drawer">
            </v-app-bar-nav-icon>
            <v-toolbar-title class="text-uppercase white--text">
                <span class="font-weight-light"> Projekt </span>
                 <span >Grupowy </span>
            </v-toolbar-title>
            <v-spacer/>
            <v-btn
              v-if="isAuth()"
              flatt
              color ="red py-2 white--text text-center"
              @click="logout()" >
                <span >Wyloguj się</span>
                <v-icon> mdi-exit-to-app</v-icon>     
            </v-btn> 
        </v-toolbar>

    <v-navigation-drawer 
        v-model="drawer"
      absolute
      temporary
      class="indigo accent-4">
            
            <v-list>
             <v-list-item v-for="link in links" :key="link.text" router :to="link.route">
              <v-list-item-action>
                <v-icon class="white--text">{{ link.icon}}</v-icon>
              </v-list-item-action>    
              <v-list-item-content>
                <v-list-item-title class="white--text">
                {{ link.text }}
                </v-list-item-title>
              </v-list-item-content>
             </v-list-item>
            </v-list>
        </v-navigation-drawer>

  </nav>
</template>


<script>
import {vm} from '../main.js'
import Auth from '../service/auth'
import { mapActions, mapGetters, mapMutations} from 'vuex';
import State from '../service/state'
export default {
  data() {
    return {
      drawer: false,
      group: null,
      links: [
        { icon: 'mdi-home', text: 'Strona główna', route: '/' },
        { icon: 'mdi-table', text: 'Lista tematów', route: '/topicsTable', requiredPerm: 'topics.view_topics' },
        { icon: 'mdi-account-group', text: 'Lista grup', route:'/groupsTable'},
        { icon: 'mdi-account-group', text: 'Twoja grupa', route:'/Groups'},
      ]
    }
  },
  methods: {
    isAuth() {
      return State.isAuth();
    },
    async logout() {
        vm.$forceUpdate();
        await Auth.logout()
        this.showMessage({ message: 'Zostałeś wylogowany!.' });
    },
    async filterAuthenticated(){
        for(let i=0; i < this.links.length; i++) {
            this.links[0].requiredPerm = 1
        }
    },
    ...mapMutations([
      'showMessage'
    ]),
    ...mapActions([
        'updateLinks',
        'updatePermissions'
    ])
    },
    computed: {
    ...mapGetters([
      'getLinksPermissions'
    ])
    },
    async created(){
        const links = await this.updatePermissions()
        await this.updateLinks(links)
    }
}
</script>