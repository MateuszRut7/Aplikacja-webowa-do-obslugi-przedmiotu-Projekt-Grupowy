<template>
  <div class="groups">
    <v-main class="elevation-3 mt-4 px-5 py-3">
      <v-row justify-center>
        <v-col cols="12" md="8" lg="6">
          <v-form v-model="formValid" ref="form">
            <!-- NAZWA GRUPY -->
            <v-text-field
              v-model="groupData.name_group"
              label="Nazwa grupy"
              :rules="[v => !!v || 'Nazwa jest wymagana']"
              required
              outlined
              class="mb-4"
            ></v-text-field>
            
            <!-- PROWADZĄCY -->
            <v-select
              v-model="selectedLecturerDisplay"
              :items="lecturerDisplayOptions"
              label="Prowadzący"
              :loading="loadingLecturers"
              :rules="[]"
              clearable
              outlined
              class="mb-4"
            >
              <template v-slot:item="{ item }">
                {{ item }}
              </template>
              <template v-slot:selection="{ item }">
                {{ item }}
              </template>
            </v-select>
            
            <!-- TEMAT -->
            <v-select
              v-model="selectedTopicDisplay"
              :items="topicDisplayOptions"
              label="Temat"
              :loading="loadingTopics"
              :rules="[]"
              clearable
              outlined
              class="mb-4"
            >
              <template v-slot:item="{ item }">
                <div>
                  <strong>{{ item.split('|')[0] }}</strong>
                  <div class="text-caption grey--text">
                    {{ item.split('|')[1] }}
                  </div>
                </div>
              </template>
              <template v-slot:selection="{ item }">
                {{ item.split('|')[0] }}
              </template>
            </v-select>
            
            <!-- PRZYCISKI -->
            <v-row class="mt-6">
              <v-col cols="12">
                <v-btn
                  color="primary"
                  :loading="loading"
                  :disabled="!formValid"
                  @click="saveGroup"
                  large
                  class="mr-3"
                >
                  <v-icon left>mdi-content-save</v-icon>
                  Zapisz
                </v-btn>
                
                <v-btn
                  @click="goBack"
                  :disabled="loading"
                  large
                  outlined
                >
                  <v-icon left>mdi-arrow-left</v-icon>
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
import axios from 'axios';
import router from '@/router';

export default {
  name: 'GroupsFormForTable',
  
  data() {
    return {
      formValid: false,
      loading: false,
      loadingLecturers: false,
      loadingTopics: false,
      
      // Wybrane wartości z dropdownów (teksty)
      selectedLecturerDisplay: null,
      selectedTopicDisplay: null,
      
      // Dane formularza
      groupData: {
        name_group: '',
        lecturer_username: null,  // username zamiast ID
        topic_id: null
      },
      
      // Mapowania
      lecturerMap: {},  // displayText → username
      topicMap: {}      // displayText → ID
    };
  },
  
  computed: {
    groupId() {
      return this.$route.params.id;
    },
    
    authToken() {
      return localStorage.getItem('access-token');
    },
    
    axiosConfig() {
      return {
        headers: {
          'Authorization': `Token ${this.authToken}`,
          'Content-Type': 'application/json'
        }
      };
    },
    
    // Opcje do wyświetlenia (computed z map)
    lecturerDisplayOptions() {
      return Object.keys(this.lecturerMap);
    },
    
    topicDisplayOptions() {
      return Object.keys(this.topicMap);
    }
  },
  
  methods: {
    goBack() {
      router.push({ name: 'GroupsTable' });
    },
    
    async loadLecturers() {
      this.loadingLecturers = true;
      try {
        // Używamy endpointu lecturers
        const response = await axios.get('/api/users/lecturers/', this.axiosConfig);
        const lecturersData = response.data; // To jest już tablica
        
        // Reset mapy
        this.lecturerMap = {};
        
        lecturersData.forEach(lecturer => {
          const displayText = `${lecturer.username} ${lecturer.first_name ? `(${lecturer.first_name} ${lecturer.last_name})` : ''}`.trim();
          const username = lecturer.username;
          
          // Dodaj do mapy: displayText → username
          this.lecturerMap[displayText] = username;
        });
        
      } catch (error) {
        console.error('Error loading lecturers:', error);
        // Fallback
        this.lecturerMap = {
          'mateusz': 'mateusz',
          'prof_nowak (Jan Nowak)': 'prof_nowak',
          'test_lecturer (Test Lecturer)': 'test_lecturer'
        };
      } finally {
        this.loadingLecturers = false;
      }
    },
    
    async loadTopics() {
      this.loadingTopics = true;
      try {
        const response = await axios.get('/api/topics/topics/', this.axiosConfig);
        const topicsData = response.data.results || response.data;
        
        // Reset mapy
        this.topicMap = {};
        
        topicsData.forEach(topic => {
          const displayText = `${topic.name_topic}|${topic.descriprion || ''}`;
          this.topicMap[displayText] = topic.id;
        });
        
      } catch (error) {
        console.error('Error loading topics:', error);
        this.topicMap = {};
      } finally {
        this.loadingTopics = false;
      }
    },
    
    async loadGroupData() {
      if (!this.groupId || this.groupId === 'new') return;
      
      try {
        const response = await axios.get(`/api/groups/groups/${this.groupId}/`, this.axiosConfig);
        const group = response.data;
        
        // Ustaw nazwę grupy
        this.groupData.name_group = group.name_group || '';
        
        // Ustaw username prowadzącego
        if (group.lecturer_display && group.lecturer_display.username) {
          this.groupData.lecturer_username = group.lecturer_display.username;
          // Znajdź matching display text
          for (const [display, username] of Object.entries(this.lecturerMap)) {
            if (username === group.lecturer_display.username) {
              this.selectedLecturerDisplay = display;
              break;
            }
          }
        } else if (group.lecturer) {
          // group.lecturer to username (np. "prof_nowak")
          this.groupData.lecturer_username = group.lecturer;
          for (const [display, username] of Object.entries(this.lecturerMap)) {
            if (username === group.lecturer) {
              this.selectedLecturerDisplay = display;
              break;
            }
          }
        }
        
        // Ustaw temat
        if (group.topic_display && group.topic_display.id) {
          this.groupData.topic_id = group.topic_display.id;
          for (const [display, id] of Object.entries(this.topicMap)) {
            if (id === group.topic_display.id) {
              this.selectedTopicDisplay = display;
              break;
            }
          }
        } else if (group.topic) {
          this.groupData.topic_id = group.topic;
          for (const [display, id] of Object.entries(this.topicMap)) {
            if (id === group.topic) {
              this.selectedTopicDisplay = display;
              break;
            }
          }
        }
        
      } catch (error) {
        console.error('Error loading group:', error);
      }
    },
    
    async saveGroup() {
      // Upewnij się, że dane są ustawione z current selection
      if (this.selectedLecturerDisplay && this.lecturerMap[this.selectedLecturerDisplay]) {
        this.groupData.lecturer_username = this.lecturerMap[this.selectedLecturerDisplay];
      }
      
      if (this.selectedTopicDisplay && this.topicMap[this.selectedTopicDisplay]) {
        this.groupData.topic_id = this.topicMap[this.selectedTopicDisplay];
      }
      
      this.loading = true;
      
      try {
        // Przygotuj dane
        const dataToSend = {
          name_group: this.groupData.name_group,
          lecturer: this.groupData.lecturer_username,  // username zamiast ID
          topic: this.groupData.topic_id
        };
        
        if (!this.groupId || this.groupId === 'new') {
          await axios.post('/api/groups/groups/', dataToSend, this.axiosConfig);
        } else {
          await axios.put(`/api/groups/groups/${this.groupId}/`, dataToSend, this.axiosConfig);
        }
        
        this.$store.commit('showMessage', { 
          message: 'Grupa zapisana pomyślnie!', 
          color: 'success' 
        });
        
        setTimeout(() => {
          router.push({ name: 'GroupsTable' });
        }, 1000);
        
      } catch (error) {
        console.error('Save error:', error);
        
        let errorMessage = 'Wystąpił błąd podczas zapisywania';
        if (error.response?.data) {
          errorMessage += ': ' + JSON.stringify(error.response.data, null, 2);
        }
        
        this.$store.commit('showMessage', { 
          message: errorMessage, 
          color: 'error' 
        });
        
      } finally {
        this.loading = false;
      }
    },
    
    async init() {
      // Najpierw załaduj listy
      await Promise.all([
        this.loadLecturers(),
        this.loadTopics()
      ]);
      
      // Potem załaduj dane grupy jeśli edytujemy
      if (this.groupId && this.groupId !== 'new') {
        await this.loadGroupData();
      }
    }
  },
  
  mounted() {
    this.init();
  },
  
  watch: {
    // Automatycznie aktualizuj username gdy zmienia się wybór prowadzącego
    selectedLecturerDisplay(newVal) {
      if (newVal && this.lecturerMap[newVal]) {
        this.groupData.lecturer_username = this.lecturerMap[newVal];
      } else {
        this.groupData.lecturer_username = null;
      }
    },
    
    // Automatycznie aktualizuj ID tematu
    selectedTopicDisplay(newVal) {
      if (newVal && this.topicMap[newVal]) {
        this.groupData.topic_id = this.topicMap[newVal];
      } else {
        this.groupData.topic_id = null;
      }
    }
  }
};
</script>

<style scoped>
.groups {
  max-width: 800px;
  margin: 0 auto;
}

.text-caption {
  font-size: 0.75rem;
  line-height: 1.2;
  margin-top: 2px;
}
</style>
