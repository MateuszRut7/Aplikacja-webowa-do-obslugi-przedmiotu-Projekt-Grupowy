<template>
  <v-footer
    dark
    padless
    app
  >
    <v-card
      class="flex"
      flat
      tile
    >
      <v-card-text class="indigo accent-4 white--text text-center">
        <h2 class="text-center">
            <strong class="subheading">Tutaj możesz nas znaleźć</strong>
        </h2>
        <v-spacer></v-spacer>

        <v-btn
         v-for="link in links"
          :key="link.icon"
          :href="link.href"
          class="subheading mx-3"
          target="_blank"
          dark
          icon
        >
          <v-icon size="24px">
            {{ link.icon }}
          </v-icon>
        </v-btn>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      group: null,
      links: [
        { icon: 'mdi-facebook', href: 'https://www.facebook.com/politechnika.warszawska' },
        { icon: 'mdi-twitter', href: 'https://twitter.com/PW_edu?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' },
        { icon: 'mdi-linkedin', href: 'https://pl.linkedin.com/school/warsaw-university-of-technology/?trk=public_profile_topcard-school' },
        { icon: 'mdi-instagram', href: 'https://www.instagram.com/politechnika_warszawska/?hl=en' },
      ]
    }
  }
}
</script>