<template>
  <div class="page-topic">
    <v-btn
      class="red py-2 white--text mr-2 my-4"
      title="Back"
      @click="back()"
    >
      <v-icon left>mdi-arrow-left</v-icon>
      Wróć
    </v-btn>
    
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="headline primary white--text">
        {{ topics.name_topic }}
      </v-card-title>
      
      <v-card-text class="pa-6">
        <v-row>
          <v-col cols="12">
            <h3 class="mb-4">Opis tematu:</h3>
            <div class="description-box pa-4">
              {{ topics.descriprion }}
            </div>
          </v-col>
        </v-row>
        
        <v-row class="mt-4">
          <v-col cols="6">
            <v-chip color="info" class="mr-2">
              <v-icon left>mdi-identifier</v-icon>
              ID: {{ topics.id }}
            </v-chip>
          </v-col>
        </v-row>
      </v-card-text>
      
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          :to="{ name: 'TopicsForm', params: { id: topics.id } }"
        >
          <v-icon left>mdi-pencil</v-icon>
          Edytuj temat
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import router from '@/router';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { objectHandler } from '@/store/utils';

export default {
  name: 'TopicsDetails',
  data() {
    return {
      topicHandler: {},
    };
  },
  methods: {
    back() {
      router.push({ name: 'TopicsTable' });
    },
    ...mapGetters([
      'getTopicsDetails',
    ]),
    ...mapMutations([
      'setTopicsDetails',
      'setTopicsDetailsProp'
    ]),
    ...mapActions([
      'fetchTopicsDetails',
      'fetchTopicsChoices'
    ]),
  },
  computed: {
    ...mapGetters({
      errors: 'getTopicsErrors',
      topicsChoices: 'getTopicsChoices'
    }),
    topicId() {
      return this.$route.params.id;
    },
    topics() {
      return new Proxy(this.getTopicsDetails(), this.topicHandler);
    },
  },
  created() {
    this.topicHandler = objectHandler(this.setTopicsDetailsProp);
    this.fetchTopicsDetails(this.topicId);
  }
};
</script>

<style scoped>
  .page-topic {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .description-box {
    background-color: #f5f5f5;
    border-radius: 8px;
    border-left: 4px solid #135C4F;
    white-space: pre-line;
    line-height: 1.6;
  }
</style>