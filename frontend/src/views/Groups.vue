<template>
  <div class="groups">
        <NoGroups
        v-if="!getHasGroup"/>
        <MyGroupe
        v-if="getHasGroup"/>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import NoGroups from '@/components/NoGroups'
import MyGroupe from '@/components/MyGroupe'
export default {
  name: 'Groups',
  components: { NoGroups, MyGroupe},
  data() {
    return {
    };
  },
  methods: {
    ...mapActions([
      'fetchUserGroup'
    ]),
  },
  computed: {
    ...mapGetters([
      'getGroupsDetails',
      'getHasGroup'
    ]),
    groupId() {
      return this.$route.params.id;
    },
  },
  created() {
    this.fetchUserGroup()
  }
};
</script>