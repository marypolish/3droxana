import { createRouter, createWebHashHistory } from 'vue-router'

import Home from './components/index.vue'
import Chat from './components/Chat.vue'
import About from './components/About.vue'
import Settings from './components/Settings.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/chat', component: Chat },
  { path: '/about', component: About },
  { path: '/settings', component: Settings },
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
