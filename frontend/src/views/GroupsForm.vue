<template>
  <div class="groups">
    <v-main class="elevation-3 mt-4 px-5 py-3">
      <v-row justify-center>
        <v-col>
          <v-form v-model="form.valid">
            <v-text-field
              v-model="groups.name_group"
              name="name"
              label="Nazwa"
              type="text"
              :error-messages="errors.name"
              maxlength="30"
            >
            </v-text-field>
            <v-spacer></v-spacer>
            <v-row>
              <v-col cols="12">
                <v-btn
                  class="mr-2 my-1"
                  color="primary"
                  title="Save"
                  :disabled="!form.valid"
                  @click="createItem(groupId, false)"
                >
                  Zapisz
                </v-btn>
                <v-btn
                  class="mr-2 my-1"
                  title="Back"
                  @click="back()"
                >
                  Wróć
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </v-main>
  </div>
</template>

<script>
import router from '@/router';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { objectHandler } from '@/store/utils';
export default {
  name: 'GroupsForm',
  data() {
    return {
      selectedFile: null,
      groupsHandler: {},
      form: {
        valid: true
      },
      rules: {
        required: value => !! value || 'To pole jest wymagane',
      },
    };
  },
  methods: {
    back() {
      router.push({ name: 'Groups' });
    },
    async createItem(groupsId) {
      let success = await this.createGroups(groupsId);
      if (success) {
        router.push({ name: 'Groups',}).catch(() => {});
      }
    },
    ...mapGetters([
      'getGroupsDetails',
    ]),
    ...mapMutations([
      'setGroupsDetails',
      'setGroupsDetailsProp'
    ]),
    ...mapActions([
      'fetchGroupsDetails',
      'createGroups',
      'fetchGroupsChoices'
    ]),
  },
  computed: {
    ...mapGetters({
      errors: 'getGroupsErrors',
      groupsChoices: 'getGroupsChoices'
    }),
    groupId() {
      return this.$route.params.id;
    },
    groups() {
      return new Proxy(this.getGroupsDetails(), this.groupHandler);
    },
  },
  created() {
    this.groupHandler = objectHandler(this.setGroupsDetailsProp);
    this.fetchGroupsDetails(this.groupId);
  }
};
</script>
