<template>
  <div class="p-6 border border-amber-200 rounded-xl bg-amber-50/50 transition-all">
    <h3 class="text-xl font-serif mb-4 text-amber-700">修改姓名</h3>
    <form @submit.prevent="changeName" class="space-y-4">
      <div>
        <label for="newName" class="block text-gray-700 mb-2">新姓名</label>
        <input
          type="text"
          id="newName"
          v-model="nameForm.newName"
          class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all"
          placeholder="请输入新姓名"
          required
        />
      </div>
      <div>
        <label for="nameVerifyPassword" class="block text-gray-700 mb-2">输入密码确认</label>
        <div class="relative">
          <input
            :type="showVerifyPassword ? 'text' : 'password'"
            id="nameVerifyPassword"
            v-model="nameForm.verifyPassword"
            class="w-full px-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all pr-10"
            placeholder="请输入当前密码"
            required
          />
          <button
            type="button"
            @click="showVerifyPassword = !showVerifyPassword"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
          >
            <i
              class="fa-fw"
              :class="showVerifyPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
            ></i>
          </button>
        </div>
      </div>
      <button
        type="submit"
        class="w-full bg-amber-700 text-white py-3 px-4 rounded-lg hover:bg-amber-800 transition-colors flex items-center justify-center"
        :disabled="nameLoading"
      >
        <i class="fa-solid fa-user-pen mr-2"></i>
        {{ nameLoading ? '处理中...' : '确认修改姓名' }}
      </button>
      <!-- 错误提示 -->
      <div v-if="nameError" class="mt-4 text-red-500 text-sm animate-pulse">
        {{ nameError }}
      </div>
      <!-- 成功提示 -->
      <div v-if="nameSuccess" class="mt-4 text-green-500 text-sm animate-pulse">
        {{ nameSuccess }}
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, defineEmits } from 'vue'
import { useUserStore } from '@/stores/user'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

const userStore = useUserStore()

// 定义Emits
const emit = defineEmits(['nameChanged'])

// 姓名修改表单
const nameForm = reactive({
  newName: '',
  verifyPassword: '',
})

// 姓名修改状态
const nameLoading = ref(false)
const nameError = ref('')
const nameSuccess = ref('')

// 密码可见性状态
const showVerifyPassword = ref(false)

// 修改姓名
const changeName = async () => {
  // 清除之前的提示
  nameError.value = ''
  nameSuccess.value = ''

  // 前端验证
  if (!nameForm.newName.trim()) {
    nameError.value = '姓名不能为空'
    return
  }

  if (nameForm.newName.length < 2) {
    nameError.value = '姓名长度至少为2位'
    return
  }

  try {
    nameLoading.value = true

    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_NAME_CHANGE), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        newName: nameForm.newName,
        currentPassword: nameForm.verifyPassword,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      // 修改成功
      nameSuccess.value = data.message || '姓名修改成功'
      // 重置表单
      nameForm.newName = ''
      nameForm.verifyPassword = ''

      // 向父组件发送成功事件
      emit('nameChanged', true)

      // 重新从后端获取用户信息以更新全局状态（TopBar和AvatarUploader都会自动更新）
      try {
        const infoResponse = await fetch('/api/user/info', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        if (infoResponse.ok) {
          const infoData = await infoResponse.json()
          if (infoData) {
            userStore.setUserInfo({
              name: infoData.name,
              studentId: infoData.studentId,
              avatarUrl: infoData.avatarUrl || '',
            })
          }
        }
      } catch (e) {
        console.error('刷新用户信息失败:', e)
      }

      // 3秒后清除成功提示
      setTimeout(() => {
        nameSuccess.value = ''
      }, 3000)
    } else {
      // 修改失败
      nameError.value = data.message || '姓名修改失败'
      emit('nameChanged', false)
    }
  } catch (error) {
    console.error('修改姓名失败:', error)
    nameError.value = '网络错误，请稍后重试'
    emit('nameChanged', false)
  } finally {
    nameLoading.value = false
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
