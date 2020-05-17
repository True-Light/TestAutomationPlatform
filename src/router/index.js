import Vue from 'vue'
import VueRouter from 'vue-router'
import login from "../components/login";
import home from "../components/home";
import ro from "element-ui/src/locale/lang/ro";

Vue.use(VueRouter)

  const routes = [
    {path: '/', redirect: '/login'},
    {path: '/login', component: login},
    {path: '/home', component: home}
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {

  if (to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()

})

export default router
