import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import Auth from '@/pages/Auth.vue'
import Home from '@/pages/Home.vue'
import Settings from '@/pages/Settings.vue'
import HistoryMuseum from '@/pages/HistoryMuseum.vue'
import CampusCheckin from '@/pages/CampusCheckin.vue'
import CollegeIntro from '@/pages/CollegeIntro.vue'
import Game from '@/pages/Game.vue'
import EndScreen from '@/pages/EndScreen.vue'
import LocationDetail from '@/pages/LocationDetail.vue'
import CollegeDetail from '@/pages/CollegeDetail.vue'
import { API_BASE_URL, API_ENDPOINTS } from '@/config/api'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/auth', name: 'auth', component: Auth },
    {
      path: '/',
      component: MainLayout,
      children: [
        { path: '', redirect: '/home' },
        { path: 'home', name: 'home', component: Home },
        { path: 'settings', name: 'settings', component: Settings },
        { path: 'history', name: 'history', component: HistoryMuseum },
        { path: 'checkin', name: 'checkin', component: CampusCheckin },
        { path: 'checkin/:id', name: 'location-detail', component: LocationDetail },
        { path: 'college', name: 'college', component: CollegeIntro },
        { path: 'college/:id', name: 'college-detail', component: CollegeDetail },
        { path: 'game', name: 'game', component: Game },
        { path: 'end', name: 'end', component: EndScreen },
      ]
    }
  ],
})

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  // 如果用户未登录且试图访问非auth页面，强制重定向到auth
  if (!token && to.name !== 'auth') {
    // 使用replace而不是push，防止用户通过浏览器后退按钮返回
    next({ name: 'auth', replace: true })
    // 确保重定向立即生效
    location.href = '/auth'
    return
  }

  // 即使有token，也验证token是否有效
  if (token && to.name !== 'auth') {
    try {
      // 发送请求验证token是否有效
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USER_INFO}`, {
        headers: { Authorization: `Bearer ${token}` },
        method: 'GET',
        // 设置超时以避免长时间等待
        signal: AbortSignal.timeout(3000)
      })

      // 如果token无效，清除token并重定向到登录页
      if (response.status === 401) {
        localStorage.removeItem('token')
        // 使用replace而不是push，防止用户通过浏览器后退按钮返回
        next({ name: 'auth', replace: true })
        // 确保重定向立即生效
        location.href = '/auth'
        return
      }
    } catch (error) {
      console.error('验证token失败:', error)
      // 发生错误时也重定向到登录页
      localStorage.removeItem('token')
      // 使用replace而不是push，防止用户通过浏览器后退按钮返回
      next({ name: 'auth', replace: true })
      // 确保重定向立即生效
      location.href = '/auth'
      return
    }
  }

  next()
})

export default router
