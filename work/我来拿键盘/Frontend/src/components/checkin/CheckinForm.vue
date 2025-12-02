<template>
  <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-md border-2 border-amber-200">
    <h2 class="text-2xl font-serif font-bold text-amber-800 mb-4">
      <i class="fa-solid fa-pen-to-square mr-2"></i>我要打卡
    </h2>

    <div class="space-y-4">
      <!-- 文字输入 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">打卡内容</label>
        <textarea
          v-model="content"
          placeholder="分享你的感受和体验..."
          class="w-full px-4 py-3 border-2 border-amber-200 rounded-lg focus:border-amber-500 focus:outline-none resize-none transition-colors"
          rows="4"
        ></textarea>
      </div>

      <!-- 图片上传 -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          上传图片 <span class="text-xs text-gray-500">(可选)</span>
        </label>
        <div class="flex items-center gap-4">
          <input
            type="file"
            @change="handleFileChange"
            accept="image/*"
            ref="fileInput"
            class="hidden"
          />
          <button
            @click="
              () => {
                const input = $refs.fileInput as HTMLInputElement
                input?.click()
              }
            "
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <i class="fa-solid fa-image mr-2"></i>选择图片
          </button>
          <span v-if="imageFile" class="text-sm text-gray-600">{{ imageFile.name }}</span>
        </div>
        <div v-if="imagePreview" class="mt-3 relative inline-block">
          <img
            :src="imagePreview"
            alt="Preview"
            class="max-w-xs rounded-lg border-2 border-amber-200"
          />
          <button
            @click="clearImage"
            class="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
          >
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="flex gap-3">
        <button
          @click="submitCheckin"
          :disabled="!content.trim() || isSubmitting"
          class="flex-1 px-6 py-3 bg-amber-700 text-white rounded-lg hover:bg-amber-800 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
        >
          <i v-if="isSubmitting" class="fa-solid fa-circle-notch fa-spin mr-2"></i>
          <span>{{ isSubmitting ? '提交中...' : '提交打卡' }}</span>
        </button>
        <button
          @click="reset"
          class="px-6 py-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          重置
        </button>
      </div>

      <!-- 提示信息 -->
      <div
        v-if="message"
        :class="messageType === 'success' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'"
        class="px-4 py-2 rounded-lg text-sm"
      >
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

const props = defineProps<{
  locationId: number
}>()

const emit = defineEmits<{
  submitted: []
}>()

const content = ref('')
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const fileInput = ref<HTMLInputElement>()

const handleFileChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    imageFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const clearImage = () => {
  imageFile.value = null
  imagePreview.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const reset = () => {
  content.value = ''
  clearImage()
  message.value = ''
}

const submitCheckin = async () => {
  if (!content.value.trim()) return

  isSubmitting.value = true
  message.value = ''

  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('locationId', props.locationId.toString())
    formData.append('content', content.value)
    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    const response = await fetch(getApiUrl(API_ENDPOINTS.CHECKIN_SUBMIT), {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (response.ok) {
      message.value = '打卡成功！'
      messageType.value = 'success'
      reset()
      emit('submitted')

      setTimeout(() => {
        message.value = ''
      }, 3000)
    } else {
      const data = await response.json()
      message.value = data.message || '打卡失败，请重试'
      messageType.value = 'error'
    }
  } catch (error) {
    console.error('Submit checkin failed:', error)
    message.value = '网络错误，请稍后重试'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}
</script>
