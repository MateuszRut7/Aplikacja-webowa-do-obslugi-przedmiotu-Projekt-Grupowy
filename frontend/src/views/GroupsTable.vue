<template>
  <div class="groups">
     <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-content='right'>
        <v-col cols="12">
        </v-col>
      </v-row>
      
      <!-- Dla wykładowców: tabela z preferencjami -->
      <template v-if="isLecturer">
        <TestTable
          :headers="headersWithPrefs"
          :items="groupsWithPrefs"
          :items-count="count"
          :get-items-per-page="itemsPerPage"
          :set-items-per-page="setGroupsItemsPerPage"
          :fetch-objects="fetchGroupsWithPreferences"
          locale="pl-PL"
          class="elevation-1"
        >
        <!-- Slot dla prowadzącego -->
        <template v-slot:item.lecturer="{ item }">
          <div v-if="item.lecturer">
            {{ item.lecturer }}
            <div v-if="item.lecturer_id" class="text-caption grey--text">
              ID: {{ item.lecturer_id }}
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak prowadzącego
          </div>
        </template>
        
        <!-- Slot dla tematu -->
        <template v-slot:item.assigned_topic.name="{ item }">
          <div v-if="item.assigned_topic">
            <strong>{{ item.assigned_topic.name }}</strong>
            <div v-if="item.assigned_topic.description" class="text-caption grey--text">
              {{ item.assigned_topic.description.substring(0, 50) }}...
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak tematu
          </div>
        </template>
        
        <template v-slot:item.preferences="{ item }">
          <div v-if="item.preferences && item.preferences.length > 0">
            <div v-for="pref in item.preferences" :key="pref.priority" class="preference-item">
              <strong>{{ pref.priority }}.</strong> {{ pref.topic_name }} (ID: {{ pref.topic_id }})
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak wybranych preferencji
          </div>
        </template>
        
        <template v-slot:item.students="{ item }">
          <div v-if="item.students && item.students.length > 0">
            <div v-for="student in item.students" :key="student.id" class="student-item">
              {{ student.first_name }} {{ student.last_name }} ({{ student.username }})
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak studentów
          </div>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            title="Usuń grupe"
            @click="deleteItem(item)"
          >
            <v-icon>
              mdi-delete
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
        </template>
        </TestTable>
      </template>
      
      <!-- Dla studentów: zwykła tabela -->
      <template v-else>
        <TestTable
          :headers="headers"
          :items="items"
          :items-count="count"
          :get-items-per-page="itemsPerPage"
          :set-items-per-page="setGroupsItemsPerPage"
          :fetch-objects="fetchGroupsList"
          locale="pl-PL"
          class="elevation-1"
        >
        <!-- Slot dla prowadzącego (dla studentów) -->
        <template v-slot:item.lecturer_display.username="{ item }">
          <div v-if="item.lecturer_display">
            {{ item.lecturer_display.username }}
            <div v-if="item.lecturer_display.first_name" class="text-caption grey--text">
              {{ item.lecturer_display.first_name }} {{ item.lecturer_display.last_name }}
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak prowadzącego
          </div>
        </template>
        
        <!-- Slot dla tematu (dla studentów) -->
        <template v-slot:item.topic_display.name_topic="{ item }">
          <div v-if="item.topic_display">
            <strong>{{ item.topic_display.name_topic }}</strong>
            <div v-if="item.topic_display.description" class="text-caption grey--text">
              {{ item.topic_display.description.substring(0, 50) }}...
            </div>
          </div>
          <div v-else class="text-caption grey--text">
            Brak tematu
          </div>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            title="Usuń grupe"
            @click="deleteItem(item)"
          >
            <v-icon>
              mdi-delete
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
        </template>
        </TestTable>
      </template>
     </v-main>
     
  </div>
</template>

<script>
// @ is an alias to /src
import TestTable from '@/components/TestTable'
import router from '@/router';
import { mapGetters, mapMutations, mapActions } from 'vuex';
export default {
  name: 'GroupsTable',
  components: { TestTable },
  data() {
    return {
      options: {}  
    };
  },
  methods: {
    ...mapMutations([
      'setGroupsItemsPerPage',
      'showMessage'
    ]),
    ...mapActions([
      'fetchGroupsList',
      'fetchGroupsWithPreferences',
      'deleteGroups',
      'updateStatusGroups'
    ]),

    editItem(item) {
      router.push({ name: 'GroupsFormForTable', params: { id: item.id } });
    },
    async deleteItem(item) {
      let confirmation = confirm('Czy na pewno chcesz usunąć grupe')
      if (confirmation) {
        await this.deleteGroups(item);
        // Ponownie pobierz odpowiednią listę
        if (this.isLecturer) {
          await this.fetchGroupsWithPreferences();
        } else {
          await this.fetchGroupsList();
        }
        this.showMessage({ message: 'Usunięto grupe' });
      }
    }, 
  },
  computed: {
    ...mapGetters({
      errors: 'getGroupsErrors',
      count:'getGroupsCount',
      headers:'getGroupsListHeaders',
      headersWithPrefs: 'getGroupsWithPrefsHeaders',
      items: 'getGroups',
      groupsWithPrefs: 'getGroupsWithPreferences',
      itemsPerPage: 'getGroupsItemsPerPage'
    }),
    
    isLecturer() {
      // Sprawdź czy użytkownik jest wykładowcą
      const permissions = this.$store.getters['getPermissions'];
      return permissions && permissions.includes && permissions.includes('lecturer');
    }
  },
  
  created() {
    // Przy montowaniu komponentu pobierz odpowiednią listę
    if (this.isLecturer) {
      this.fetchGroupsWithPreferences();
    }
  }
};
</script>

<style>
  .groups {
    width:70%; 
    margin-left:15%; 
    margin-right:150%;
  }
  .preference-item {
    font-size: 0.85rem;
    margin-bottom: 2px;
  }
  .student-item {
    font-size: 0.8rem;
    margin-bottom: 2px;
  }
</style>
