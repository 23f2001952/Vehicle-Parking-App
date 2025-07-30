import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import { router } from './routes.js'
import { auth } from './auth.js'  
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css';
import { getToast } from './toast.js'


router.beforeEach((to, from, next) => {
  const isLoggedIn = auth.loggedIn
  const userRole = auth.role
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const roleRequired = to.meta.role
  const toast = getToast()
  console.log(to)
   if (requiresAuth && !isLoggedIn) {
    toast.error('You are not logged in!')

    return next('/login')
  }

  if ((to.path === '/login' || to.path === '/register') && isLoggedIn) {
  toast.info('You are already logged in!')
  return next('/')
}

  if (roleRequired && userRole !== roleRequired) {
    toast.warning('You don’t have permission for this page')
    return next('/')
  }
  next()
});

createApp(App).use(router).use(ToastPlugin).mount('#app')


