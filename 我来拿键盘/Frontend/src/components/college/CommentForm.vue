<template>
  <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
      rows="3"
    ></textarea>

    <div class="flex justify-end gap-2 mt-3">
      <button
        v-if="parentId"
        @click="$emit('cancel')"
        class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
      >
        取消
      </button>
      <button
        @click="submitComment"
        :disabled="!content.trim() || isSubmitting"
        class="px-6 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        {{ isSubmitting ? '提交中...' : '发表评论' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

const props = defineProps<{
  collegeId: number
  parentId?: number
  placeholder?: string
}>()

const emit = defineEmits<{
  submitted: []
  cancel: []
}>()

const content = ref('')
const isSubmitting = ref(false)

const submitComment = async () => {
  if (!content.value.trim()) return

  isSubmitting.value = true

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.COLLEGE_COMMENT), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        collegeId: props.collegeId,
        parentId: props.parentId || null,
        content: content.value,
      }),
    })

    if (response.ok) {
      content.value = ''
      emit('submitted')
    } else {
      alert('评论失败，请重试')
    }
  } catch (error) {
    console.error('Failed to submit comment:', error)
    alert('网络错误，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>
