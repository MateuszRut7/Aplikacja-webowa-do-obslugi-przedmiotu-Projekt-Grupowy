<template>
  <div class="topics">
     <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-content='right'>
        <v-col cols="12">
          <v-btn
            class="mr-2 my-4"
            color="primary"
            :to="{ name: 'TopicsForm' }"
          >
            Dodaj
          </v-btn>
        </v-col>
      </v-row>
      <TestTable
        :headers="headers"
        :items="items"
        :items-count="count"
        :get-items-per-page="itemsPerPage"
        :set-items-per-page="setTopicsItemsPerPage"
        :fetch-objects="fetchTopicsList"
        locale="pl-PL"
        class="elevation-1"
      >
      <template v-slot:item.actions="{ item }">

        <v-btn
          icon
          title="Szczegóły projektu"
          @click="itemDetails(item)"
        >
          <v-icon>
            mdi-note
          </v-icon>
        </v-btn>

        <v-btn
          icon
          title="Edytuj projekt"
          @click="editItem(item)"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
        <v-btn
          icon
          title="Usuń projekt"
          @click="deleteItem(item)"
        >
          <v-icon>
            mdi-delete
          </v-icon>
        </v-btn>
      </template>
      </TestTable>
     </v-main>

  </div>
</template>

<script>
// @ is an alias to /src
import TestTable from '@/components/TestTable'
import router from '@/router';
import { mapGetters, mapMutations, mapActions } from 'vuex';
export default {
  name: 'TopicsTable',
  components: { TestTable },
  data() {
    return {
      options: {}  
      
    };
  },
  watch: {
      dialogDetails (val) {
        val || this.closeDetails()
      },
    },
  methods: {
    ...mapMutations([
      'setTopicsItemsPerPage',
      'showMessage'
    ]),
    ...mapActions([
      'fetchTopicsList',
      'deleteTopics',
      "fetchTopicsChoices",
      'updateStatusTopics'
    ]),
    async itemDetails(item){
      router.push({ name: 'TopicsDetails', params: { id: item.id } });
    },

    editItem(item) {
      router.push({ name: 'TopicsForm', params: { id: item.id } });
    },
    async deleteItem(item) {
      let confirmation = confirm('Czy na pewno chcesz usunąć projekt?')
      if (confirmation) {
        await this.deleteTopics(item);
        this.fetchTopicsList()
        this.showMessage({ message: 'Usunięto projekt' });
      }
    }, 
  },
  computed: {
    ...mapGetters({
      errors: 'getTopicsErrors',
      count:'getTopicsCount',
      headers:'getTopicsListHeaders',
      items: 'getTopics',
      itemsPerPage: 'getTopicsItemsPerPage'
    }),
  },
};
</script>

<style>
  .topics {
    width:70%; 
    margin-left:15%; 
    margin-right:150%;
  }
</style>