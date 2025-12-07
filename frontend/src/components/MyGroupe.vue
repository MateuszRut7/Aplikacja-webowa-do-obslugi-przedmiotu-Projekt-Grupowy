<template>
  <div class="groups">
    <v-card>
      <v-card-title>{{groups.name_group}}</v-card-title>
      <v-row>
        <v-col md="3" offset-md="1">
          <h3>Kod grupy: {{groups.code}}</h3>
        </v-col>
        <v-col offset-md="5">
          <v-btn class="red py-2 white--text mr- my-4" @click="leave()">
            Opuść Grupe
          </v-btn>
        </v-col>
      </v-row>
      
      <!-- KOMUNIKATY -->
      <v-row v-if="selectionError">
        <v-col>
          <v-alert type="error" dense>{{ selectionError }}</v-alert>
        </v-col>
      </v-row>
      
      <v-row v-if="selections.length > 0">
        <v-col>
          <v-alert type="info" dense>
            <h4>Twoje wybory tematów:</h4>
            <div v-for="(sel, idx) in selections" :key="idx" class="mt-1">
              <strong>{{ sel.priority }}.</strong> {{ sel.topic.name_topic }} (ID: {{ sel.topic.id }})
            </div>
          </v-alert>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col>
          <StudentsTableComponent/>
        </v-col>
        <v-col>
          <!-- PRZEKAZUJEMY WYBORY DO TopicsTableComponent -->
          <TopicsTableComponent 
            ref="topicsTable"
            @selections-changed="onSelectionsChanged"
            :current-selections="selections"
          />
        </v-col>
      </v-row>
      
      <v-row>
        <v-col offset-md="9">
          <!-- ZMIENIAMY WARUNEK NA selections.length === 3 -->
          <v-btn 
            class="green py-2 white--text mr- my-4" 
            @click="send()" 
            :disabled="selections.length !== 3 || !!selectionError"
          >
            Zatwierdź wybór ({{ selections.length }}/3)
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import router from '@/router';
import { mapGetters, mapMutations, mapActions } from 'vuex';
import { objectHandler } from '@/store/utils';
import StudentsTableComponent from '@/components/StudentsTableComponent'
import TopicsTableComponent from '@/components/TopicsTableComponent'
import axios from 'axios';

export default {
  name: 'MyGroupe',
  components: { StudentsTableComponent, TopicsTableComponent },

  data() {
    return {
      groupsHandler: {},
      form: {
        valid: true
      },
      rules: {
        required: value => !! value || 'To pole jest wymagane',
      },
      selections: [], // {topic: {...}, priority: 1/2/3}
      selectionError: ''
    };
  },
  
  methods: {
    // ODBIERAMY WYBORY Z TopicsTableComponent
    onSelectionsChanged(newSelections) {
      console.log('Otrzymano nowe selekcje:', newSelections);
      // DEBUG: sprawdź strukturę
      if (newSelections.length > 0) {
        console.log('Przykładowy topic:', newSelections[0].topic);
        console.log('Czy ma id?', 'id' in newSelections[0].topic);
        console.log('Wszystkie klucze:', Object.keys(newSelections[0].topic));
      }
      this.selections = newSelections;
      this.validateSelections();
    },
    
    // WALIDUJEMY WYBORY
    validateSelections() {
      if (this.selections.length !== 3) {
        this.selectionError = 'Wybierz dokładnie 3 tematy!';
        return false;
      }
      
      // Sprawdź czy są 3 różne priorytety
      const priorities = this.selections.map(sel => sel.priority);
      const uniquePriorities = [...new Set(priorities)];
      
      if (uniquePriorities.length !== 3) {
        this.selectionError = 'Musisz wybrać 3 różne priorytety (1, 2, 3)!';
        return false;
      }
      
      // Sprawdź czy priorytety to 1,2,3
      const sortedPriorities = [...priorities].sort((a, b) => a - b);
      if (sortedPriorities[0] !== 1 || sortedPriorities[1] !== 2 || sortedPriorities[2] !== 3) {
        this.selectionError = 'Użyj priorytetów 1, 2 i 3!';
        return false;
      }
      
      this.selectionError = '';
      return true;
    },
    
    // FUNKCJA ZATWIERDZANIA WYBORU - POPRAWIONA
    async send() {
      try {
        if (!this.validateSelections()) {
          this.showMessage({ 
            message: this.selectionError, 
            color: 'error' 
          });
          return;
        }
        
        console.log('Zatwierdzam wybory tematów:', this.selections);
        console.log('Szczegółowo selections[0]:', JSON.stringify(this.selections[0], null, 2));
        
        // PRZYGOTUJ DANE - DEBUG
        const preferencesData = {
          group_id: this.groups.id,
          preferences: this.selections.map(sel => {
            console.log('Mapping selection:', sel);
            console.log('Topic object:', sel.topic);
            console.log('Topic ID:', sel.topic.id);
            return {
              topic_id: sel.topic.id,
              priority: sel.priority
            };
          })
        };
        
        console.log('Wysyłam do backendu:', preferencesData);
        
        // WYŚLIJ DO BACKENDU - UŻYJ RELATIVE URL
        const token = localStorage.getItem('access-token');
        const response = await axios.post(
          '/api/preferences/preferences/save-preferences/',  // RELATIVE URL - Vue proxy
          preferencesData,
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        console.log('Odpowiedź z backendu:', response.data);
        
        this.showMessage({ 
          message: 'Preferencje tematów zostały zapisane!', 
          color: 'success' 
        });
        
        // Pokaż podsumowanie
        const summary = this.selections
          .map(sel => `${sel.priority}. ${sel.topic.name_topic} (ID: ${sel.topic.id})`)
          .join('\n');
        
        alert(`Twoje wybory zostały zapisane:\n\n${summary}`);
        
      } catch (error) {
        console.error('Błąd zatwierdzania wyborów:', error);
        console.error('Error response:', error.response);
        
        let errorMessage = 'Błąd zapisywania preferencji';
        
        if (error.response && error.response.data) {
          if (error.response.data.error) {
            errorMessage = error.response.data.error;
          } else if (error.response.data.non_field_errors) {
            errorMessage = error.response.data.non_field_errors.join(', ');
          } else if (error.response.data.detail) {
            errorMessage = error.response.data.detail;
          }
        } else if (error.message) {
          errorMessage = error.message;
        }
        
        this.showMessage({ 
          message: errorMessage, 
          color: 'error' 
        });
      }
    },

    back() {
      router.push({ name: 'GroupsTable' });
    },
    
    async createItem(groupsId) {
      let success = await this.createGroups(groupsId);
      if (success) {
        router.push({ name: 'GroupsTable' }).catch(() => {});
      }
    },
    
    async leave() {
      await this.leaveGroup();
      await this.fetchUserGroup();
    },
    
    ...mapGetters([
      'getGroupsDetails',
    ]),
    
    ...mapMutations([
      'setGroupsDetails',
      'setGroupsDetailsProp',
      'showMessage'
    ]),
    
    ...mapActions([
      'fetchGroupsDetailsForUser',
      'createGroups',
      'fetchGroupsChoices',
      'leaveGroup',
      'fetchUserGroup'
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
    this.fetchGroupsDetailsForUser();
  }
};
</script>
