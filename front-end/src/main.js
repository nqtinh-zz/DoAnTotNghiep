// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import './plugins/vuetify'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import 'font-awesome/css/font-awesome.min.css'
import store from './store'
import axios from 'axios'
import LanguageSwitch from '@/components/common/LanguageSwitch'
import FlagIcon from 'vue-flag-icon'
import VeeValidate from 'vee-validate'
import { i18n } from '@/plugins/i18n'
import VueLazyload from 'vue-lazyload'
import setAuthToken from './utils/setAuthToken'
Vue.prototype.$http = axios
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}
Vue.use(FlagIcon)
Vue.use(Vuetify)
Vue.use(VueLazyload)
Vue.use(VeeValidate)
Vue.component('langx', LanguageSwitch)
Vue.config.productionTip = false

const checkToken = () => {
  if (localStorage.getItem('expiration_date'))
  {
    let tmp = new Date(localStorage.getItem('expiration_date')).getTime()
  let now = new Date().getTime()
  if (tmp - now < 0)
  {
    console.log('time out')
    axios({
      url: `${HTTP_API}/api/user/logout`,
      method: 'GET'
    })
      .then(data => {
        localStorage.clear()
        setAuthToken()
        location.reload()
        console.log('time out okkkkkkkkkkkkkkk')
      })
  }
  // setTimeout(checkToken, 1000 * 60 * 30);
  }
};

checkToken();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  i18n,
  store,
  components: { App },
  template: '<App/>'
})
