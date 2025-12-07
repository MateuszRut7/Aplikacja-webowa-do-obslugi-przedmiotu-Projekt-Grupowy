<template>
   <v-main class="elevation-0 mt-4 px-5 py-3">
      <v-row justify-center>
        <v-col>
          <h2>Podaj login i hasło</h2>
          <v-form v-model="form.valid">
            <v-text-field
              v-model="username"
              name='Hasło'
              label='Login'
              type="text"
              :rules="[rules.required]"
              maxlength="30"
            >
            </v-text-field>
            <v-text-field
              v-model="password"
              name="nazwisko"
              label="Hasło"
              type="password"
              maxlength="30"
              :rules="[rules.required]"
            >
            </v-text-field>  
            <v-row>
              <v-col cols="12">
                <v-btn
                  class="mr-2 my-3"
                  color="primary"
                  title="Zapisz"
                  :disabled="!form.valid"
                  @click="loginTo()"
                >
                  Zaloguj
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
    </v-main> 
</template>

<script>
import Auth from '../service/auth';
import { mapMutations, mapActions } from 'vuex';
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      form: {
        valid: true
      },
      rules: {
        required: value => !! value || 'To pole jest wymagane',
      },
    };
  },
  methods: {
    async loginTo() {
      try {
        await Auth.login(this.username, this.password);
        this.showMessage({ message: 'Zalogowano.' });
      } catch (err) {
        this.showMessage({ message: 'Niepoprawny login lub hasło.', color: 'error' });
      }
    },
    ...mapMutations([
      'showMessage'
    ]),
    ...mapActions([
      'login',
    ]),
  },
};
</script>
