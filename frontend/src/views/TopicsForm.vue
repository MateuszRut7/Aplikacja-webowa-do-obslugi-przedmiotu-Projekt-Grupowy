<template>
  <div class="topics">
    <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-center>
        <v-col>
          <h2>{{ formTitle }}</h2>
          <v-form v-model="form.valid">
            <v-text-field
              v-model="topics.name_topic"
              name='name_topic'
              label='Nazwa tematu'
              type="text"
              :rules="[rules.required, rules.maxLength60]"
              maxlength="60"
              counter
              :error-messages="errors.name_topic"
            >
            </v-text-field>
            <v-textarea
              v-model="topics.descriprion"
              name="descriprion"
              label="Opis"
              type="text"
              :rules="[rules.required, rules.maxLength300]"
              maxlength="300"
              counter
              rows="3"
              :error-messages="errors.descriprion"
            >
            </v-textarea>
            <v-row>
              <v-col cols="12">
                <v-btn
                  class="mr-2 my-3"
                  color="primary"
                  title="Zapisz"
                  :disabled="!form.valid"
                  @click="saveItem(topicsId)"
                >
                  Zapisz
                </v-btn>
                <v-btn
                  class="mr-2 my-3"
                  color="secondary"
                  title="Anuluj"
                  @click="back()"
                >
                  Anuluj
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
  name: 'TopicsForm',
  data() {
    return {
      topicsHandler: {},
      form: {
        valid: true
      },
      rules: {
        required: value => !! value || 'To pole jest wymagane',
        maxLength60: value => !value || value.length <= 60 || 'Maksymalnie 60 znaków',
        maxLength300: value => !value || value.length <= 300 || 'Maksymalnie 300 znaków'
      }
    };
  },
  watch: {
      dialogDetails (val) {
        val || this.closeDetails()
      },
    },
  methods: {
    back() {
      router.push({ name: 'TopicsTable' });
    },
    
    async saveItem(topicsId) {
      let success = await this.createTopics(topicsId);
      if (success) {
        router.push({ name: 'TopicsTable' }).catch(() => {});
      }
    },
    
    ...mapGetters([
      'getTopicsDetails',
    ]),
    
    ...mapMutations([
      'setTopicsDetails',
      'setTopicsDetailsProp',
      'showMessage'
    ]),
    
    ...mapActions([
      'fetchTopicsDetails',
      'createTopics',
      'fetchTopicsChoices'
    ]),
  },
  
  computed: {
    ...mapGetters({
      errors: 'getTopicsErrors',
      topicsChoices: 'getTopicsChoices'
    }),
    
    topicsId() {
      return this.$route.params.id;
    },
    
    formTitle() {
      return this.topicsId ? 'Edycja tematu' : 'Nowy temat';
    },
    
    topics() {
      return new Proxy(this.getTopicsDetails(), this.topicsHandler);
    },
  },
  
  created() {
    this.topicsHandler = objectHandler(this.setTopicsDetailsProp);
    this.fetchTopicsDetails(this.topicsId);
  }
};
</script>
