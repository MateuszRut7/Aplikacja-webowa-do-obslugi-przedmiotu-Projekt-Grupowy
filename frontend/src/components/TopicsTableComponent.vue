<template>
  <div class="topics">
    <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-content='right'>
        <v-col cols="12">
          <v-alert v-if="selectionError" type="error" dense>
            {{ selectionError }}
          </v-alert>
          <v-alert v-if="selections.length > 0" type="info" dense>
            Wybrane tematy: 
            <span v-for="(sel, idx) in selections" :key="idx" class="ml-2">
              {{ idx + 1 }}. {{ sel.topic.name_topic }}
            </span>
            <v-btn 
              small 
              @click="clearAllSelections" 
              color="error" 
              class="ml-4"
              title="Wyczyść wszystkie wybory"
            >
              <v-icon small>mdi-close</v-icon>
              Wyczyść
            </v-btn>
          </v-alert>
        </v-col>
      </v-row>
      <TestTable
        :headers="headersWithSelection"
        :items="items"
        :items-count="count"
        :get-items-per-page="itemsPerPage"
        :set-items-per-page="setTopicsItemsPerPage"
        :fetch-objects="fetchTopicsList"
        locale="pl-PL"
        class="elevation-1"
      >
      <!-- Slot dla nazwy tematu - klikalny -->
      <template v-slot:item.name_topic="{ item }">
        <div class="d-flex align-center">
          <a 
            href="#" 
            @click.prevent="showTopicDetails(item)"
            class="topic-name-link mr-2"
            title="Kliknij aby zobaczyć szczegóły tematu"
          >
            {{ item.name_topic }}
          </a>
          <v-btn
            icon
            x-small
            @click="showTopicDetails(item)"
            title="Szczegóły tematu"
            class="ml-1"
          >
            <v-icon x-small>mdi-information</v-icon>
          </v-btn>
        </div>
      </template>
      
      <!-- Slot dla wyboru tematów -->
      <template v-slot:item.selection="{ item }">
        <!-- PRZYCISKI WYBORU 1, 2, 3 -->
        <v-btn
          v-for="priority in [1, 2, 3]"
          :key="priority"
          small
          :color="getButtonColor(item, priority)"
          class="ml-1"
          @click="selectTopic(item, priority)"
          :disabled="isTopicSelected(item) || isPriorityTaken(priority)"
        >
          {{ priority }}
        </v-btn>
        
        <!-- PRZYCISK USUNIĘCIA WYBORU -->
        <v-btn
          v-if="isTopicSelected(item)"
          icon
          small
          color="error"
          class="ml-1"
          @click="removeSelection(item)"
          title="Usuń wybór"
        >
          <v-icon small>mdi-close</v-icon>
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
import State from '@/service/state'; // DODANO IMPORT STATE

export default {
  name: 'TopicsTableComponent',
  components: { TestTable },
  
  data() {
    return {
      options: {},
      selections: this.loadSelections(), // Ładuj z localStorage przy starcie
      selectionError: ''
    };
  },
  
  computed: {
    ...mapGetters({
      errors: 'getTopicsErrors',
      count:'getTopicsCount',
      headers:'getTopicsListHeaders',
      items: 'getTopics',
      itemsPerPage: 'getTopicsItemsPerPage'
    }),
    
    // Poprawione nagłówki
    headersWithSelection() {
      // Zostawiamy tylko kolumnę "Nazwa" z oryginalnych headers
      const baseHeaders = this.headers.filter(h => h.value === 'name_topic');
      
      return [
        ...baseHeaders,
        { text: 'Wybór', value: 'selection', sortable: false, width: '250px' }
      ];
    }
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
    
    // Przejdź do szczegółów tematu
    showTopicDetails(item) {
      router.push({ name: 'TopicsDetails', params: { id: item.id } });
    },

    async deleteItem(item) {
      let confirmation = confirm('Czy na pewno chcesz usunąć projekt?')
      if (confirmation) {
        await this.deleteTopics(item);
        this.fetchTopicsList()
        this.showMessage({ message: 'Usunięto projekt' });
      }
    },
    
    // ========== METODY DO ZAPISYWANIA WYBORÓW ==========
    
    // Pobierz klucz localStorage na podstawie username
    getStorageKey() {
      const username = State.getUsername() || 'unknown';
      return `topicSelections_${username}`;
    },
    
    // Zapisz wybory do localStorage (PER UŻYTKOWNIK)
    saveSelections() {
      if (this.selections.length > 0) {
        const key = this.getStorageKey();
        // Zapisz tylko potrzebne dane (nie cały obiekt topic)
        const serialized = this.selections.map(sel => ({
          topicId: sel.topic.id,
          priority: sel.priority,
          topicName: sel.topic.name_topic
        }));
        localStorage.setItem(key, JSON.stringify(serialized));
        console.log('Zapisano wybory do localStorage dla użytkownika:', State.getUsername());
      } else {
        const key = this.getStorageKey();
        localStorage.removeItem(key);
        console.log('Usunięto wybory z localStorage dla użytkownika:', State.getUsername());
      }
    },
    
    // Załaduj wybory z localStorage (PER UŻYTKOWNIK)
    loadSelections() {
      const key = this.getStorageKey();
      const saved = localStorage.getItem(key);
      if (!saved) {
        console.log('Brak zapisanych wyborów w localStorage dla:', State.getUsername());
        return [];
      }
      
      try {
        const parsed = JSON.parse(saved);
        console.log('Załadowano zapisane wybory z localStorage dla:', State.getUsername());
        
        // Na tym etapie mamy tylko ID tematów, pełne obiekty zostaną dodane w syncSelectionsWithItems
        return parsed.map(item => ({
          topic: { id: item.topicId, name_topic: item.topicName },
          priority: item.priority
        }));
      } catch (e) {
        console.error('Błąd ładowania zapisanych wyborów:', e);
        localStorage.removeItem(key); // Usuń uszkodzone dane
        return [];
      }
    },
    
    // Synchronizuj wybory z załadowanymi tematami
    syncSelectionsWithItems() {
      if (!this.items || this.items.length === 0) {
        console.log('Brak tematów do synchronizacji');
        return;
      }
      
      if (this.selections.length === 0) return;
      
      console.log('Synchronizuję wybory z aktualną listą tematów...');
      
      // Mapowanie ID tematów do pełnych obiektów
      const topicMap = {};
      this.items.forEach(topic => {
        topicMap[topic.id] = topic;
      });
      
      // Filtruj i aktualizuj wybory
      const updatedSelections = [];
      this.selections.forEach(selection => {
        const topicId = selection.topic.id;
        if (topicMap[topicId]) {
          // Znaleziono temat w aktualnej liście - aktualizuj pełny obiekt
          updatedSelections.push({
            topic: topicMap[topicId],
            priority: selection.priority
          });
          console.log(`Przywrócono wybór: ${topicMap[topicId].name_topic} (priorytet ${selection.priority})`);
        } else {
          console.warn(`Temat ID ${topicId} nie istnieje w aktualnej liście, pomijam...`);
        }
      });
      
      // Sortuj po priorytecie
      updatedSelections.sort((a, b) => a.priority - b.priority);
      
      // Zaktualizuj selections
      this.selections = updatedSelections;
      
      // Zapisz zsynchronizowane wybory
      this.saveSelections();
      
      // Powiadom rodziców o zmianie
      this.$emit('selections-changed', this.selections);
      
      console.log('Zsynchronizowano wybory:', this.selections);
    },
    
    // Wyczyść wszystkie wybory
    clearAllSelections() {
      if (confirm('Czy na pewno chcesz wyczyścić wszystkie wybory tematów?')) {
        const key = this.getStorageKey();
        this.selections = [];
        localStorage.removeItem(key);
        this.$emit('selections-changed', []);
        this.selectionError = '';
        this.showMessage({ message: 'Wyczyszczono wszystkie wybory tematów' });
      }
    },
    
    // ========== METODY DO WYBORU TEMATÓW ==========
    
    // Sprawdź czy temat jest już wybrany
    isTopicSelected(topic) {
      return this.selections.some(sel => sel.topic.id === topic.id);
    },
    
    // Sprawdź czy priorytet jest już zajęty
    isPriorityTaken(priority) {
      return this.selections.some(sel => sel.priority === priority);
    },
    
    // Pobierz kolor przycisku
    getButtonColor(topic, priority) {
      const selection = this.selections.find(sel => 
        sel.topic.id === topic.id && sel.priority === priority
      );
      return selection ? 'primary' : 'grey lighten-2';
    },
    
    // Wybierz temat z priorytetem
    selectTopic(topic, priority) {
      // Usuń stary wybór z tego priorytetu jeśli istnieje
      this.selections = this.selections.filter(sel => sel.priority !== priority);
      
      // Dodaj nowy wybór
      this.selections.push({
        topic: topic,
        priority: priority
      });
      
      // Sortuj po priorytecie
      this.selections.sort((a, b) => a.priority - b.priority);
      
      // Zapisz do localStorage
      this.saveSelections();
      
      // Wyślij wybory do parent component (MyGroupe.vue)
      this.$emit('selections-changed', this.selections);
      
      this.selectionError = '';
      console.log(`Wybrano temat ${topic.name_topic} z priorytetem ${priority}`);
    },
    
    // Usuń wybór tematu
    removeSelection(topic) {
      this.selections = this.selections.filter(sel => sel.topic.id !== topic.id);
      this.saveSelections();
      this.$emit('selections-changed', this.selections);
      this.selectionError = '';
      console.log(`Usunięto wybór tematu: ${topic.name_topic}`);
    },
    
    // Sprawdź czy wybory są poprawne
    validateSelections() {
      if (this.selections.length !== 3) {
        this.selectionError = 'Wybierz dokładnie 3 tematy!';
        return false;
      }
      
      const priorities = this.selections.map(sel => sel.priority);
      if (new Set(priorities).size !== 3) {
        this.selectionError = 'Wybierz 3 różne priorytety (1, 2, 3)!';
        return false;
      }
      
      this.selectionError = '';
      return true;
    }
  },
  
  watch: {
    // Automatycznie zapisuj przy każdej zmianie selections
    selections: {
      handler() {
        this.validateSelections();
        this.saveSelections();
      },
      deep: true
    },
    
    // Synchronizuj wybory gdy załadują się tematy
    items: {
      handler(newItems) {
        if (newItems && newItems.length > 0) {
          // Opóźnienie aby mieć pewność że komponent jest gotowy
          setTimeout(() => {
            this.syncSelectionsWithItems();
          }, 300);
        }
      },
      immediate: true
    }
  },
  
  // Hook lifecycle - synchronizuj przy montowaniu
  mounted() {
    console.log('TopicsTableComponent zamontowany, wybory:', this.selections);
    console.log('Aktualny użytkownik:', State.getUsername());
  }
};
</script>

<style scoped>
  .topics {
    width: 70%; 
    margin-left: 15%; 
    margin-right: 150%;
  }
  
  .topic-name-link {
    color: #135C4F; /* Kolor zgodny z theme.primary */
    text-decoration: none;
    font-weight: 500;
    cursor: pointer;
    transition: color 0.3s;
  }
  
  .topic-name-link:hover {
    color: #FD5523; /* Kolor zgodny z theme.secondary */
    text-decoration: underline;
  }
</style>
