import Vue from 'vue'
import VueRouter from 'vue-router'
import login from "../components/login";
import home from "../components/home";
import ro from "element-ui/src/locale/lang/ro";
import welcome from "../components/welcome";
import todayWork from "../components/workReport/todayWork";
import workProject from "../components/workReport/workProject";
import showInterfaceProject from "../components/interfaceTest/showInterfaceProject";
import InterfaceCase from "../components/interfaceTest/InterfaceCase";
import searchWebCase from "../components/webTest/searchWebCase";
import webCase from "../components/webTest/webCase";
import runningTask from "../components/celeryTask/runningTask";
import setTask from "../components/celeryTask/setTask";
import taskResult from "../components/celeryTask/taskResult";
import newPerformance from "../components/performanceTest/newPerformance";
import searchPerformanceCase from "../components/performanceTest/searchPerformanceCase";
import sysConfig from "../components/sysConfig";

Vue.use(VueRouter)

  const routes = [
    {path: '/', redirect: '/login'},
    {path: '/login', component: login},
    {path: '/home',
      component: home,
      redirect: '/welcome',
      children: [
        {path: '/welcome', component: welcome},
        {path: '/todayWork', component: todayWork},
        {path: '/historyWork', component: workProject},
        {path: '/interfaceProject', component: showInterfaceProject},
        {path: '/interfaceCase', component: InterfaceCase},

        {path: '/newWebCase', component: searchWebCase},
        {path: '/checkWebCase', component: webCase},
        {path: '/checkTask', component: runningTask},
        {path: '/setTask', component: setTask},
        {path: '/checkResult', component: taskResult},
        {path: '/newPerformance', component: newPerformance},
        {path: '/checkPerformance', component: searchPerformanceCase},

        {path: '/sysConfig', component: sysConfig}

      ]}
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
