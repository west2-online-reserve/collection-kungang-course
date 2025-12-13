<template>
  <div
    class="mb-10 p-6 border border-amber-200 rounded-xl bg-amber-50/50 transition-all hover:shadow-md animate-fade-in slide-up animation-delay-100"
  >
    <h3 class="text-xl font-serif mb-4 text-amber-700">修改头像</h3>
    <div class="flex flex-col items-center">
      <div class="relative mb-4">
        <div
          v-if="displayAvatar"
          class="w-28 h-28 rounded-full overflow-hidden border-4 border-amber-100 shadow-md"
        >
          <img :src="displayAvatar" alt="用户头像" class="w-full h-full object-cover" />
        </div>
        <div
          v-else
          class="w-28 h-28 rounded-full border-4 border-amber-100 shadow-md bg-white flex items-center justify-center text-amber-700"
        >
          <svg
            width="56"
            height="56"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <circle cx="12" cy="8" r="4" />
            <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
          </svg>
        </div>
        <div
          class="absolute bottom-0 right-0 bg-amber-700 text-white rounded-full p-2 cursor-pointer hover:bg-amber-800 transition-colors"
          @click="openFileInput"
        >
          <i class="fa-solid fa-camera"></i>
          <input
            type="file"
            ref="fileInput"
            accept="image/*"
            class="hidden"
            @change="handleFileSelect"
          />
        </div>
      </div>
      <!-- 用户信息显示 -->
      <div class="text-center mt-2 mb-2">
        <div class="font-medium text-amber-800">{{ userStore.userName || '加载中...' }}</div>
        <div class="text-lg text-gray-600">{{ userStore.studentId || '加载中...' }}</div>
      </div>

      <!-- 上传状态提示 -->
      <div v-if="uploadStatus" class="mt-3 px-4 py-2 rounded-lg text-sm" :class="uploadStatusClass">
        <i
          class="fa-solid mr-2"
          :class="
            uploadStatus === 'success'
              ? 'fa-circle-check'
              : uploadStatus === 'error'
                ? 'fa-circle-exclamation'
                : 'fa-spinner fa-spin'
          "
        ></i>
        {{ uploadMessage }}
      </div>
    </div>
  </div>

  <!-- 头像裁剪弹窗 -->
  <Teleport to="body">
    <AvatarCropper
      v-if="showPreviewModal"
      :image-src="previewImage"
      @confirm="confirmImage"
      @cancel="closePreviewModal"
    />
  </Teleport>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, onMounted, reactive, computed } from 'vue'
import { getApiUrl, getStaticUrl, API_ENDPOINTS, STATIC_ENDPOINTS } from '@/config/api'
import AvatarCropper from './AvatarCropper.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 定义Props
const props = defineProps<{
  userAvatar: string
}>()

// 定义Emits
const emit = defineEmits<{
  avatarUpdate: [newAvatar: string]
}>()

// 用户信息
const userInfo = reactive({
  studentId: '',
  name: '',
})

// 头像相关
const fileInput = ref<HTMLInputElement>()
const previewImage = ref<string>('')
const showPreviewModal = ref<boolean>(false)
const uploadStatus = ref<'uploading' | 'success' | 'error' | null>(null)
const uploadMessage = ref<string>('')

// 上传状态样式
const uploadStatusClass = computed(() => {
  switch (uploadStatus.value) {
    case 'success':
      return 'bg-green-100 text-green-700 border border-green-300'
    case 'error':
      return 'bg-red-100 text-red-700 border border-red-300'
    case 'uploading':
      return 'bg-blue-100 text-blue-700 border border-blue-300'
    default:
      return ''
  }
})

// 显示的头像 - 优先使用 store 中的头像
const displayAvatar = computed(() => {
  const url = userStore.avatarUrl || props.userAvatar
  console.log('AvatarUploader - 合并后的头像URL:', url)
  if (!url) {
    console.log('AvatarUploader - 无头像URL，返回空字符串')
    return ''
  }
  // 如果不是完整URL，则添加后端基础URL
  if (!url.startsWith('http') && !url.startsWith('https')) {
    const fullUrl = getApiUrl(url)
    console.log('AvatarUploader - 构建完整URL:', fullUrl)
    return fullUrl
  }
  console.log('AvatarUploader - 使用完整URL:', url)
  return url
})

// 刷新用户信息的方法
const refreshUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      const response = await fetch('/api/user/info', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        if (data) {
          userInfo.studentId = data.studentId || ''
          userInfo.name = data.name || ''
          // 更新 store
          userStore.setUserInfo({
            studentId: data.studentId,
            name: data.name,
            avatarUrl: data.avatarUrl || '',
          })
        }
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 暴露方法供外部调用
defineExpose({
  refreshUserInfo,
})

// 获取用户信息
onMounted(async () => {
  await refreshUserInfo()
})

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]

    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      uploadStatus.value = 'error'
      uploadMessage.value = '请选择图片文件'
      setTimeout(() => {
        uploadStatus.value = null
      }, 3000)
      return
    }

    // 验证文件大小 (5MB)
    const maxSize = 5 * 1024 * 1024
    if (file.size > maxSize) {
      uploadStatus.value = 'error'
      uploadMessage.value = '图片大小不能超过 5MB'
      setTimeout(() => {
        uploadStatus.value = null
      }, 3000)
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target?.result as string
      showPreviewModal.value = true
    }
    reader.readAsDataURL(file)
  }
}

// 打开文件选择器
const openFileInput = () => {
  fileInput.value?.click()
}

// 关闭预览弹窗
const closePreviewModal = () => {
  showPreviewModal.value = false
  previewImage.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 确认使用图片
const confirmImage = async (croppedData: string) => {
  if (!croppedData) return

  uploadStatus.value = 'uploading'
  uploadMessage.value = '正在上传头像...'

  try {
    const token = localStorage.getItem('token')

    // 将 base64 转换为 blob
    const res = await fetch(croppedData)
    const blob = await res.blob()

    // 创建 FormData
    const formData = new FormData()
    formData.append('avatar', blob, 'avatar.png')

    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_AVATAR_UPLOAD), {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (response.ok) {
      const data = await response.json()

      // 更新全局 store
      userStore.updateAvatar(data.avatarUrl)

      // 向父组件发送新头像URL
      emit('avatarUpdate', data.avatarUrl)

      uploadStatus.value = 'success'
      uploadMessage.value = '头像上传成功！'

      // 3秒后清除成功提示
      setTimeout(() => {
        uploadStatus.value = null
      }, 3000)

      showPreviewModal.value = false
    } else {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || '头像上传失败')
    }
  } catch (error) {
    console.error('上传头像失败:', error)
    uploadStatus.value = 'error'
    uploadMessage.value = error instanceof Error ? error.message : '上传头像失败，请重试'

    // 5秒后清除错误提示
    setTimeout(() => {
      uploadStatus.value = null
    }, 5000)
  } finally {
    // 关闭预览
    showPreviewModal.value = false
    previewImage.value = ''
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}
</script>

<style scoped>
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
</style>
