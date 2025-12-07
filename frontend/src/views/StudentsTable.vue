<template>
  <div class="students">
     <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-content='right'>
        <v-col cols="12">
          <v-btn
            class="mr-2 my-4"
            color="primary"
            :to="{ name: 'Students' }"
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
        :set-items-per-page="setStudentsItemsPerPage"
        :fetch-objects="fetchStudentsList"
        locale="pl-PL"
        class="elevation-1"
      >
      <template v-slot:item.actions="{ item }">
        <v-btn
          icon
          title="Edytuj Studenta"
          @click="editItem(item)"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
        <v-btn
          icon
          title="Usuń studenta"
          @click="deleteItem(item)"
        >
          <v-icon>
            mdi-account-cancel
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
  name: 'StudentsTable',
  components: { TestTable },
  data() {
    return {
      options: {}  
    };
  },
  methods: {
    ...mapMutations([
      'setStudentsItemsPerPage',
      'showMessage'
    ]),
     ...mapActions([
      'fetchStudentsList',
      'deleteStudents',
      "fetchStudentsChoices",
      'updateStatusStudents'
    ]),
    editItem(item) {
      router.push({ name: 'Students', params: { id: item.id } });
    },
     async deleteItem(item) {
      let confirmation = confirm('Czy na pewno chcesz usunąć studenta')
      if (confirmation) {
        await this.deleteStudents(item);
        this.fetchStudentsList()
        this.showMessage({ message: 'Usunięto studenta' });
      }
    }, 
  },
  computed: {
    ...mapGetters({
      errors: 'getStudentsErrors',
      count:'getStudentsCount',
      headers:'getStudentsListHeaders',
      items: 'getStudents',
      itemsPerPage: 'getStudentsItemsPerPage'
    }),
  },
};
</script>