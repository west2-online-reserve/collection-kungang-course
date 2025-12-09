<!-- components/Navbar.vue -->
<template>
  <nav class="navbar" :class="{ 'navbar-scrolled': isScrolled }">
    <div class="navbar-container">
      <!-- Logo区域 -->
      <div class="navbar-brand">
        <img src="/logo.png" alt="Logo" class="logo-image" />
        <!-- <div class="logo-placeholder">{{ title }}</div> -->
      </div>

      <!-- 导航菜单 -->
      <div class="navbar-menu">
        <ul class="navbar-nav">
          <li v-for="item in navItems" :key="item.id" class="nav-item">
            <a
              href="#"
              class="nav-link"
              :class="{ active: currentPage === item.page }"
              @click.prevent="changePage(item.page)"
            >
              {{ item.name }}
            </a>
          </li>
        </ul>
      </div>

      <!-- 右侧功能区 -->
      <div class="navbar-actions">
        <!-- 用户信息 -->
        <div class="user-menu">
          <button class="user-toggle" @click="toggleUserMenu">
            <div class="user-avatar-placeholder">
              {{ user.name?.charAt(0) || 'U' }}
            </div>
            <span class="user-name">{{ user.name || '用户' }}</span>
          </button>

          <div class="user-dropdown" :class="{ active: isUserMenuOpen }">
            <div class="user-info">
              <div class="user-avatar-placeholder large">
                {{ user.name?.charAt(0) || 'U' }}
              </div>
              <div class="user-details">
                <h4>{{ user.name || '用户' }}</h4>
              </div>

              <div class="menu_button">
                <button @click="handleMenuClick('profile')">个人资料</button>
                <button @click="handleMenuClick('feedback')">反馈</button>
                <button @click="handleLogout">退出登录</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import './styles/NavBar.css'
import type { NavItem } from '@/types/nav'





// Props
defineProps({
  brandName: {
    type: String,
    default: '我的应用',
  },
  navItems: {
    type: Array<NavItem>,
    default: () => [],
  },
  user: {
    type: Object,
    default: () => ({}),
  },
  currentPage: {
    type: String,
    default: 'home',
  },
})

// Emits
const emit = defineEmits(['page-change', 'menu-click', 'logout'])

// 响应式数据
const isScrolled = ref(false)
const isMenuOpen = ref(false)
const isUserMenuOpen = ref(false)

// 方法


const changePage = (page: string) => {
  emit('page-change', page)
  // console.log('切换到页面:', props.currentPage)
  closeMobileMenu()
}

const closeMobileMenu = () => {
  isMenuOpen.value = false
}

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const handleMenuClick = (action: string) => {
  emit('menu-click', action)
  isUserMenuOpen.value = false
}

const handleLogout = () => {
  emit('logout')
  isUserMenuOpen.value = false
}

// 滚动监听
const handleScroll = () => {
  isScrolled.value = window.scrollY > 10
}

// 点击外部关闭菜单
const handleClickOutside = (event: MouseEvent) => {
  if (!(event.target as HTMLElement).closest('.user-menu')) {
    isUserMenuOpen.value = false;
  }
}

// 生命周期
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* 样式与之前相同，保持简洁 */

</style>
