import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
//global css
import './css/global.css'
// fonts
import './assets/fonts/iconfont.css'

import axios from 'axios'

//base url
axios.defaults.baseURL = 'http://192.168.3.2:8000/'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
