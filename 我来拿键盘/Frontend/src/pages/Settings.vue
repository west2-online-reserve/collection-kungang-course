<template>
  <div class="min-h-screen bg-parchment relative overflow-hidden">
    <div
      class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1529590003495-2e0a378906d1?q=80&w=1920&auto=format&fit=crop')] bg-center bg-cover opacity-40"
    ></div>
    <div
      class="relative z-10 max-w-3xl mx-auto mt-24 p-8 rounded-2xl bg-white/90 border border-black/10 shadow-xl mb-16 animate-fade-in slide-up"
    >
      <div class="text-2xl font-serif mb-8 text-amber-800">个人设置</div>

      <!-- 头像上传组件 -->
      <AvatarUploader
        ref="avatarUploaderRef"
        :user-avatar="userAvatar"
        @avatar-update="handleAvatarUploaded"
      />

      <!-- 选项卡选择区域 -->
      <div class="mb-6 flex flex-wrap gap-3 animate-fade-in slide-up animation-delay-200">
        <button
          @click="activeTab = 'password'"
          class="px-5 py-3 rounded-lg transition-all duration-300 flex items-center"
          :class="{
            'bg-amber-700 text-white shadow-md': activeTab === 'password',
            'bg-gray-100 text-gray-700 hover:bg-gray-200': activeTab !== 'password',
          }"
        >
          <i class="fa-solid fa-lock mr-2"></i>
          修改密码
        </button>
        <button
          @click="activeTab = 'name'"
          class="px-5 py-3 rounded-lg transition-all duration-300 flex items-center"
          :class="{
            'bg-amber-700 text-white shadow-md': activeTab === 'name',
            'bg-gray-100 text-gray-700 hover:bg-gray-200': activeTab !== 'name',
          }"
        >
          <i class="fa-solid fa-user-pen mr-2"></i>
          修改姓名
        </button>
      </div>

      <!-- 选项卡内容区域 -->
      <div class="tab-container">
        <transition name="page-fade" mode="out-in">
          <!-- 密码修改组件 -->
          <PasswordChangeForm
            v-if="activeTab === 'password'"
            :loading="isLoading"
            :error="passwordError"
            :success="passwordSuccess"
            @change-password="handleChangePassword"
          />

          <!-- 姓名修改组件 -->
          <NameChangeForm
            v-else-if="activeTab === 'name'"
            :loading="nameLoading"
            :error="nameError"
            :success="nameSuccess"
            @change-name="handleChangeName"
          />
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'
import AvatarUploader from '@/components/settings/AvatarUploader.vue'
import PasswordChangeForm from '@/components/settings/PasswordChangeForm.vue'
import NameChangeForm from '@/components/settings/NameChangeForm.vue'

const userStore = useUserStore()

// 组件引用
const avatarUploaderRef = ref<InstanceType<typeof AvatarUploader>>()

// 用户头像 - 从 store 获取
const userAvatar = ref<string>('')

// 状态管理
const isLoading = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')
const nameLoading = ref(false)
const nameError = ref('')
const nameSuccess = ref('')
const activeTab = ref('password')

// 处理头像上传成功 - 不需要做任何事，store 已经更新
const handleAvatarUploaded = (avatarUrl: string) => {
  // Store 已经在 AvatarUploader 中更新，这里可以留空或做其他处理
  console.log('Avatar updated:', avatarUrl)
}

// 处理密码修改
const handleChangePassword = async (passwordData: {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}) => {
  // 清除之前的提示
  passwordError.value = ''
  passwordSuccess.value = ''

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
        currentPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      // 修改成功
      passwordSuccess.value = data.message || '密码修改成功'

      // 刷新用户信息（虽然密码不显示，但保持一致性）
      await avatarUploaderRef.value?.refreshUserInfo()

      // 3秒后清除成功提示
      setTimeout(() => {
        passwordSuccess.value = ''
      }, 3000)
    } else {
      // 修改失败
      passwordError.value = data.message || '密码修改失败'
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    passwordError.value = '网络错误，请稍后重试'
  } finally {
    isLoading.value = false
  }
}

// 处理姓名修改
const handleChangeName = async (nameData: { newName: string; verifyPassword: string }) => {
  // 清除之前的提示
  nameError.value = ''
  nameSuccess.value = ''

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
        newName: nameData.newName,
        verifyPassword: nameData.verifyPassword,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      // 修改成功
      nameSuccess.value = data.message || '姓名修改成功'

      // 更新全局 store（通过刷新用户信息）
      await avatarUploaderRef.value?.refreshUserInfo()

      // 3秒后清除成功提示
      setTimeout(() => {
        nameSuccess.value = ''
      }, 3000)
    } else {
      // 修改失败
      nameError.value = data.message || '姓名修改失败'
    }
  } catch (error) {
    console.error('修改姓名失败:', error)
    nameError.value = '网络错误，请稍后重试'
  } finally {
    nameLoading.value = false
  }
}

// 初始化时获取用户信息
const initUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_INFO), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      const data = await response.json()
      if (data.avatar) {
        userAvatar.value = data.avatar
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 页面加载时初始化用户信息
initUserInfo()
</script>

<style scoped>
/* 页面过渡动画 - 淡入效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 弹性显示动画 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 通用动画类 */
.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
  opacity: 0;
}

.slide-up {
  animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  opacity: 0;
}

/* 延迟动画类 */
.animation-delay-100 {
  animation-delay: 0.5s;
}

.animation-delay-200 {
  animation-delay: 0.1s;
}

.animation-delay-300 {
  animation-delay: 0.15s;
}

/* 确保选项卡容器有足够的高度防止内容跳动 */
.tab-container {
  position: relative;
  min-height: 450px;
  overflow: hidden;
}

/* 确保过渡动画元素正确定位 */
.page-fade-enter-active,
.page-fade-leave-active {
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
}

/* 确保离开动画在上方 */
.page-fade-leave-active {
  z-index: 1;
}

/* 确保选项卡容器有定位上下文 */
.tab-container {
  position: relative;
  min-height: 400px;
}

/* 增强弹窗弹性动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 优化预览弹窗的弹性动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from {
  transform: scale(0.95) translateY(20px);
  opacity: 0;
}

.modal-leave-to {
  transform: scale(0.95) translateY(20px);
  opacity: 0;
}

/* 头像上传动画 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

/* 相机图标悬停效果增强 */
.relative:hover .absolute {
  animation: pulse 1.5s infinite;
}

/* 选项卡按钮效果增强 */
button.active {
  transform: translateY(-2px);
}
</style>
