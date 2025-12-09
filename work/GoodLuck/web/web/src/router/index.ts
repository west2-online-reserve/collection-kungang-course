// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/LoginPage.vue'
import Main from '../views/MainPage.vue'
import Admin from '../views/AdminPage.vue'

import profile from '../views/ProfilePage.vue'
import { authAPI } from '@/utils/api'
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/main',
    name: 'Main',
    component: Main,
    meta: {
          KeepAlive: true
    }

  },
  {
    path:'/profile',
    name:'Profile',
    component: profile,

  },
  {
    path:'/admin',
    name:'admin',
    component:Admin,
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const checkAuth = async (token: string) => {
  try {
  await authAPI.verifyToken(token);
  }
  catch  {
    return false
  }
  return true
}
const token = localStorage.getItem('token')||'';
const valid = await checkAuth(token);
// 添加路由守卫
router.beforeEach((to, from, next) => {
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (token==='') {
      next('/login')
    } else {
     if (valid) {
        next()
      } else {
        next('/login')
      }
    }
  } else {
    next()
  }
})

export default router
