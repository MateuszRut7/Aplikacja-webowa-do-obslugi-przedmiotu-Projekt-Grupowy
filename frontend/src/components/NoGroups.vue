
<template>
  <v-row justify="center">
    <v-col
      cols="12"
      sm="10"
      md="8"
      lg="6"
    >
      <v-card ref="form">
        <v-card-text>
          <v-text-field
            ref="code"
            v-model="code"
            :rules="[() => !!code || 'Nie wpisano kodu']"
            :error-messages="errorMessages"
            label="Kod grupy"
            required
          >
                <template slot="append-outer">
                    <v-btn
                    dark x-large
                    color="primary"
                    text
                    @click="join"
                    >
                        Dołącz
                    </v-btn>
                </template>
            </v-text-field>
        
        </v-card-text>
        <div >
            <v-btn
                dark x-large
                color ="green py-2 white--text text-center"
                text
                :to="{ name: 'GroupsForm' }"
            >
                Utwórz nową grupę
            </v-btn>
        </div>
        <v-divider class="mt-12"></v-divider>
        <v-card-actions>
          <v-slide-x-reverse-transition>
            <v-tooltip
              v-if="formHasErrors"
              left
            >
            </v-tooltip>
          </v-slide-x-reverse-transition>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
  import { mapActions }  from 'vuex';
  import router from '@/router';
  export default {
    data: () => ({
      name: 'NoGroups',
      errorMessages: '',
      code: null,
      formHasErrors: false,
    }),
    methods: {
      async join () {
        await this.joinGroup(this.code)
        router.push({ name: 'Groups' });
        this.fetchUserGroup()
      },
      ...mapActions([
      'joinGroup',
      'fetchUserGroup'
    ]),
    },
  }
</script>
