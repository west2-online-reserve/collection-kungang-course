import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/animals'
      },
      {
        path: 'animals',
        name: 'Animals',
        component: () => import('../views/Animals.vue')
      },
      {
        path: 'animals/:id',
        name: 'AnimalDetail',
        component: () => import('../views/AnimalDetail.vue')
      },
      {
        path: 'feed-records',
        name: 'FeedRecords',
        component: () => import('../views/FeedRecords.vue')
      },
      {
        path: 'health-logs',
        name: 'HealthLogs',
        component: () => import('../views/HealthLogs.vue'),
        meta: { roles: ['admin', 'volunteer'] }
      },
      {
        path: 'adoptions',
        name: 'Adoptions',
        component: () => import('../views/Adoptions.vue')
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('../views/UserManagement.vue'),
        meta: { roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.roles) {
    const roleMap = { 'admin': '管理员', 'volunteer': '志愿者', 'user': '普通用户' }
    const allowedRoles = to.meta.roles.map(r => roleMap[r] || r)
    if (!allowedRoles.includes(authStore.user?.role)) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
