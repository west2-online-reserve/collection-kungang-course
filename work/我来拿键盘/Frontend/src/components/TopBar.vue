<template>
  <button
    v-if="ui.topBarCollapsed"
    @click="toggleTopBar"
    class="fixed top-2 z-[50]"
    :class="{ 'transition-all duration-300': isMounted }"
    :style="{ left: toggleButtonLeft, transform: 'translateX(-50%)' }"
  >
    <div
      class="w-10 h-10 bg-amber-700 hover:bg-amber-800 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-300 backdrop-blur-sm border border-amber-600"
    >
      <i class="fa-solid fa-chevron-down text-sm"></i>
    </div>
  </button>

  <!-- 顶部栏 -->
  <div
    :class="[
      'fixed left-0 right-0 bg-white/60 backdrop-blur-md border-b border-black/10 z-[50] rounded-b-xl',
      isMounted ? 'transition-all duration-300' : '',
      ui.topBarCollapsed ? 'top-0 h-0 overflow-hidden' : 'top-0 h-14',
    ]"
    :style="topStyle"
  >
    <div class="h-full px-4 flex items-center justify-between relative">
      <!-- 左侧 Logo -->
      <div class="flex items-center gap-3">
        <i class="fa-solid fa-landmark text-2xl text-amber-700"></i>
      </div>

      <!-- 收起按钮：顶部栏展开时显示（永远在底部中央） -->
      <button
        v-if="!ui.topBarCollapsed"
        @click="toggleTopBar"
        class="fixed z-[50] transition-opacity duration-300"
        :style="{
          left: toggleButtonLeft,
          bottom: '-20px',
          transform: 'translateX(-50%)',
          opacity: isMounted ? 1 : 0,
        }"
      >
        <div
          class="w-10 h-10 bg-amber-700 hover:bg-amber-800 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-300 backdrop-blur-sm border border-amber-600"
        >
          <i class="fa-solid fa-chevron-up text-sm"></i>
        </div>
      </button>

      <!-- 头像 / 用户菜单 -->
      <div class="relative">
        <div
          ref="avatarBtn"
          @click="toggleProfile"
          class="w-10 h-10 rounded-full overflow-hidden border border-black/10 shadow cursor-pointer"
        >
          <img v-if="avatarUrl" :src="avatarUrl" alt="avatar" class="w-full h-full object-cover" />
          <div v-else class="w-full h-full flex items-center justify-center text-black/70">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="8" r="4" />
              <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
            </svg>
          </div>
        </div>

        <!-- 用户管理菜单 -->
        <transition name="profile">
          <div
            v-if="ui.profileOpen"
            ref="profileCard"
            class="absolute right-0 mt-2 w-56 bg-white/95 border border-black/10 rounded-xl shadow-xl z-[60]"
          >
            <div class="p-4 space-y-2">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full overflow-hidden border border-black/10">
                  <img
                    v-if="avatarUrl"
                    :src="avatarUrl"
                    alt="avatar"
                    class="w-full h-full object-cover"
                  />
                  <div v-else class="w-full h-full flex items-center justify-center text-black/70">
                    <svg
                      width="18"
                      height="18"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="8" r="4" />
                      <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
                    </svg>
                  </div>
                </div>
                <div>
                  <div class="font-medium">{{ userName }}</div>
                  <div class="text-sm text-gray-600">{{ studentId }}</div>
                </div>
              </div>

              <button @click="toSettings" class="w-full py-2 rounded-lg bg-black text-white mb-2">
                设置
              </button>

              <button
                @click="logout"
                class="w-full py-2 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition-colors"
              >
                注销
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

const ui = useUiStore()
const userStore = useUserStore()
const router = useRouter()

const avatarUrl = computed(() => {
  // 确保头像URL是完整的后端URL
  const url = userStore.avatarUrl
  console.log('TopBar - userStore.avatarUrl原始值:', url)
  if (!url) {
    console.log('TopBar - URL为空，返回空字符串')
    return ''
  }
  // 如果不是完整URL，则添加后端基础URL
  if (!url.startsWith('http') && !url.startsWith('https')) {
    const fullUrl = getApiUrl(url)
    console.log('TopBar - 构建完整URL:', fullUrl)
    return fullUrl
  }
  console.log('TopBar - 使用完整URL:', url)
  return url
})
const userName = computed(() => userStore.userName || '姓名')
const studentId = computed(() => userStore.studentId || '学号')

const topStyle = computed(() => ({
  paddingLeft: ui.navExpanded ? '12rem' : '3rem',
}))

const toggleButtonLeft = computed(() => {
  const offset = ui.navExpanded ? 12 : 3
  return `calc(50% + ${offset / 2}rem)`
})

const avatarBtn = ref<HTMLElement | null>(null)
const profileCard = ref<HTMLElement | null>(null)
const isMounted = ref(false)

function toSettings() {
  router.push('/settings')
  ui.setProfileOpen(false)
}

function logout() {
  localStorage.removeItem('token')
  userStore.clearUserInfo()
  router.push('/auth')
  ui.setProfileOpen(false)
}

function toggleProfile() {
  ui.setProfileOpen(!ui.profileOpen)
}

function toggleTopBar() {
  ui.toggleTopBar()
}

function onDocClick(e: MouseEvent) {
  const t = e.target as Node
  if (profileCard.value?.contains(t)) return
  if (avatarBtn.value?.contains(t)) return
  ui.setProfileOpen(false)
}

onMounted(async () => {
  // 延迟启用动画，防止初始加载时的跳动
  setTimeout(() => {
    isMounted.value = true
  }, 100)

  document.addEventListener('mousedown', onDocClick)

  try {
    const token = localStorage.getItem('token')
    if (token) {
      const r = await fetch(getApiUrl(API_ENDPOINTS.USER_INFO), {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (r.ok) {
        const d = await r.json()
        userStore.setUserInfo({
          name: d.name,
          studentId: d.studentId,
          avatarUrl: d.avatarUrl || '',
        })
      } else if (r.status === 401) {
        // 强制重定向到登录页，不等待用户操作
        console.log('Token无效或已过期，强制重定向到登录页')
        localStorage.removeItem('token')
        userStore.clearUserInfo()
        // 使用replace而不是push，防止用户通过浏览器后退按钮返回
        router.replace('/auth')
        // 确保重定向立即生效
        location.href = '/auth'
      }
    }
  } catch (e) {
    console.error('获取用户信息失败:', e)
    // 强制重定向到登录页，不等待用户操作
    localStorage.removeItem('token')
    userStore.clearUserInfo()
    // 使用replace而不是push，防止用户通过浏览器后退按钮返回
    router.replace('/auth')
    // 确保重定向立即生效
    location.href = '/auth'
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onDocClick)
})
</script>

<style scoped>
.profile-enter-active {
  animation: profileDown 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
.profile-leave-active {
  animation: profileUp 0.2s cubic-bezier(0.645, 0.045, 0.355, 1) forwards;
}

@keyframes profileDown {
  0% {
    transform: translateY(-8px);
    opacity: 0;
  }
  60% {
    transform: translateY(6px);
    opacity: 1;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes profileUp {
  0% {
    transform: translateY(0);
    opacity: 1;
  }
  40% {
    transform: translateY(6px);
    opacity: 0.8;
  }
  100% {
    transform: translateY(-12px);
    opacity: 0;
  }
}
</style>
