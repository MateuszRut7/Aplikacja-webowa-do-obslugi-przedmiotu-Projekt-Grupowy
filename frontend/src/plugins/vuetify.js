import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import pl from 'vuetify/es5/locale/pl';

Vue.use(Vuetify);

const light = {
  primary: '#135C4F',
  secondary: '#FD5523'
};

export default new Vuetify({
  theme: { 
    themes: { light }
  },
  lang: {
    locales: { pl },
    current: 'pl'
  },
  icons: {
    iconfont: 'mdi',
  },
});