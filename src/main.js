import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
//global css
import './css/global.css'
import './css/index.scss'
// fonts
import './assets/fonts/iconfont.css'

import axios from 'axios'

//base url
// axios.defaults.baseURL = 'http://192.168.3.2/api/'
axios.defaults.baseURL = 'http://10.71.82.65/api/'


// axios.defaults.proxy = {
//   '/api': {
//     target: 'http://192.168.3.2:8000/api',
//     changeOrigin: true,
//     pathRewrites: {
//       '^/api': 'http://192.168.3.2:8000/api'
//     }
//   }
// }

// 挂载拦截器
axios.interceptors.request.use(config => {
  //console.log(config)
  config.headers.Authorization = window.sessionStorage.getItem('token')
  // config.headers['Access-Control-Allow-Origin'] = "*"
  return config
})

Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
