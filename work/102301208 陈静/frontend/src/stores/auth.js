import { defineStore } from 'pinia'
import axios from '../utils/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === '管理员',
    isVolunteer: (state) => state.user?.role === '管理员'  // 只有管理员才有志愿者权限
  },
  
  actions: {
    async login(username, password) {
      const response = await axios.post('/api/login', { username, password })
      this.token = response.data.token
      this.user = response.data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    
    async register(userData) {
      await axios.post('/api/register', userData)
    },
    
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
