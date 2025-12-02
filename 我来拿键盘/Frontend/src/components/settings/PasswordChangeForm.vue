<template>
  <div class="p-6 border border-amber-200 rounded-xl bg-amber-50/50 transition-all">
    <h3 class="text-xl font-serif mb-4 text-amber-700">修改密码</h3>
    <form @submit.prevent="changePassword" class="space-y-4">
      <div>
        <label for="currentPassword" class="block text-gray-700 mb-2">当前密码</label>
        <div class="relative">
          <input
            :type="showCurrentPassword ? 'text' : 'password'"
            id="currentPassword"
            v-model="passwordForm.currentPassword"
            class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all pr-10"
            placeholder="请输入当前密码"
            required
          />
          <button
            type="button"
            @click="showCurrentPassword = !showCurrentPassword"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <i
              class="fa-fw"
              :class="showCurrentPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
            ></i>
          </button>
        </div>
      </div>
      <div>
        <label for="newPassword" class="block text-gray-700 mb-2">新密码</label>
        <div class="relative">
          <input
            :type="showNewPassword ? 'text' : 'password'"
            id="newPassword"
            v-model="passwordForm.newPassword"
            class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all pr-10"
            placeholder="请输入新密码"
            required
          />
          <button
            type="button"
            @click="showNewPassword = !showNewPassword"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <i
              class="fa-fw"
              :class="showNewPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
            ></i>
          </button>
        </div>
      </div>
      <div>
        <label for="confirmPassword" class="block text-gray-700 mb-2">确认新密码</label>
        <div class="relative">
          <input
            :type="showConfirmPassword ? 'text' : 'password'"
            id="confirmPassword"
            v-model="passwordForm.confirmPassword"
            class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all pr-10"
            placeholder="请再次输入新密码"
            required
          />
          <button
            type="button"
            @click="showConfirmPassword = !showConfirmPassword"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <i
              class="fa-fw"
              :class="showConfirmPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
            ></i>
          </button>
        </div>
      </div>
      <button
        type="submit"
        class="w-full bg-amber-700 text-white py-3 px-4 rounded-lg hover:bg-amber-800 transition-colors flex items-center justify-center"
        :disabled="isLoading"
      >
        <i class="fa-solid fa-lock mr-2"></i>
        {{ isLoading ? '处理中...' : '确认修改密码' }}
      </button>
      <!-- 错误提示 -->
      <div v-if="passwordError" class="mt-4 text-red-500 text-sm animate-pulse">
        {{ passwordError }}
      </div>
      <!-- 成功提示 -->
      <div v-if="passwordSuccess" class="mt-4 text-green-500 text-sm animate-pulse">
        {{ passwordSuccess }}
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, defineEmits } from 'vue'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

// 定义Emits
const emit = defineEmits(['passwordChanged'])

// 密码修改表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

// 密码修改状态
const isLoading = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

// 密码可见性状态
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// 修改密码
const changePassword = async () => {
  // 清除之前的提示
  passwordError.value = ''
  passwordSuccess.value = ''

  // 前端验证
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }

  if (passwordForm.newPassword.length < 6) {
    passwordError.value = '新密码长度至少为6位'
    return
  }

  try {
    isLoading.value = true

    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_PASSWORD_CHANGE), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        currentPassword: passwordForm.currentPassword,
        newPassword: passwordForm.newPassword,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      // 修改成功
      passwordSuccess.value = data.message || '密码修改成功'
      // 重置表单
      passwordForm.currentPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''

      // 向父组件发送成功事件
      emit('passwordChanged', true)

      // 3秒后清除成功提示
      setTimeout(() => {
        passwordSuccess.value = ''
      }, 3000)
    } else {
      // 修改失败
      passwordError.value = data.message || '密码修改失败'
      emit('passwordChanged', false)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    passwordError.value = '网络错误，请稍后重试'
    emit('passwordChanged', false)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 错误和成功提示动画 */
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 1.5s infinite;
}
</style>
