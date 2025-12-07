<template>
  <v-app class="grey lighten-4">
    <v-snackbar
      top
      v-model="snackbar"
      :color="snackbarColor">{{ snackbarMessage }}
    </v-snackbar>
    <v-main>
      <Navbar 
      v-if="isAuth()"/>
      <v-content class="mx-4 mb-4">
        <router-view></router-view>
      </v-content>
      
      <Footer />
    </v-main> 
  </v-app>
</template>

<script>
import Footer from './components/Footer.vue';
import Navbar from './components/Navbar.vue';
import { mapGetters, mapMutations } from 'vuex';
import State from '@/service/state';

export default {
  name: 'App',

  components: {
    Navbar,
    Footer,
    
  },

   data() {
    return {};
  },
  computed: {
    snackbar: {
      get() {
        return this.isSnackbarOpened;
      },
      set() {
        this.hideMessage();
      }
    },
    currentRouteName() {
        return this.$route.name;
    },
    ...mapGetters([
      'isSnackbarOpened'
    ]),
    ...mapGetters({
      snackbarMessage: 'getSnackbarMessage',
      snackbarColor: 'getSnackbarColor'
    })
  },
  methods: {
    ...mapMutations([
      'hideMessage'
    ]),
    isAuth() {
      return State.isAuth();
    },
  }
};
</script>

