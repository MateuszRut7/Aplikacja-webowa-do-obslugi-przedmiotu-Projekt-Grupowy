
<template>
  <div class="home" >
    <v-card
      class=" mx-auto blue--text"
      elevation="12"
      height="auto"
      max-width="900"
    >
      <h1 class="text-center">Cele przedmiotu</h1>
      <v-container class=" ">
        <h3>
          • Zapoznanie studentów z popularnymi metodykami zarządzania projektami zespołowymi (krótko waterfall, głównie metodyki zwinne jak np. Scrum)
        </h3>

        <h3 class="my-5">
          • Zapoznanie studentów z narzędziami informatycznymi wspomagającymi prowadzenie projektów zespołowych
        </h3>

        <h3 class="my-5">
          • Praktyczne utrwalenie umiejętności korzystania z narzędzi do wersjonowania kodów źródłowych oraz innych dokumentów projektowych
        </h3>

        <h3 class="my-5">
          • Omówienie wybranych zagadnień związanych z projektami opensource/openhardware – np. kwestia praw autorskich, licencjonowanie, zarządzanie, dobieranie zespołu, itp.
        </h3>

        <h3 class="my-5">
          • Praktyczne ugruntowanie wiedzy nt. metodyk prowadzenia projektów jak i tej pochodzącej z innych przedmiotów
        </h3>

        <h3 class="my-5">
          • Zapoznanie studentów z różnymi pracownikami naukowymi wydziału oraz obszarami prowadzonych badań, w celu bardziej świadomego podjęcia decyzji o wyborze promotora
        </h3>

        <h3 class="my-5"> 
          •zwiększenie aktywności studentów w kołach naukowych
        </h3>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import State from '../service/state'
  export default {
    data: () => ({
      //
    }),
  methods: {
    ...mapGetters([
      'getPermissions'
    ]),
    ...mapActions([
      'updatePermissions',
      'updateLinks'
    ]),
  },
  async created() {
    const permissions = await this.updatePermissions();
    this.updateLinks(permissions)
    State.setPermissions(permissions);
  }
  }
</script>

<style>
  .home {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
</style>