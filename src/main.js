import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import './plugins/element.js'
import ElementUI, {Message, MessageBox} from 'element-ui'
//global css
import './css/global.css'
import 'element-ui/lib/theme-chalk/index.css'
// import './css/index.scss'
// fonts
import './assets/fonts/iconfont.css'

import axios from 'axios'


Vue.use(ElementUI)
Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm

//base url
axios.defaults.baseURL = 'http://192.168.3.2:8888/api/'
// axios.defaults.baseURL = 'http://10.71.82.65/api/'
// axios.defaults.baseURL = 'http://127.0.0.1:8888/api/'


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
