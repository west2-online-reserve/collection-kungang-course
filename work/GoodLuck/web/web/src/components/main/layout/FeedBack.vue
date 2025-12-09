<template>
  <!-- 反馈弹窗遮罩层 -->
  <div v-if="visible" class="feedback-modal-mask" >
    <div class="feedback-modal" @click.stop>
      <!-- 弹窗头部 -->
      <div class="modal-header">
        <h2>意见反馈</h2>
        <button class="close-btn" @click="handleClose">
          <i class="icon-close"></i>
        </button>
      </div>

      <!-- 弹窗内容 -->
      <div class="modal-content">
        <div class="form-group">
          <label for="feedback-content">反馈内容 <span class="required">*</span></label>
          <textarea
            id="feedback-content"
            v-model="feedbackForm.content"
            class="feedback-textarea"
            placeholder="请详细描述您遇到的问题或建议..."
            rows="4"
            maxlength="500"
          ></textarea>
          <div class="char-count">{{ feedbackForm.content.length }}/500</div>
        </div>

        <div class="form-group">
          <label for="email">邮箱地址</label>
          <input
            id="email"
            v-model="feedbackForm.email"
            type="email"
            class="email-input"
            placeholder="选填，方便我们回复您"
          />
        </div>
      </div>

      <!-- 弹窗底部按钮 -->
      <div class="modal-footer">
        <button class="cancel-btn" @click="handleClose">取消</button>
        <button
          class="submit-btn"
          :disabled="!feedbackForm.content.trim() || submitting"
          @click="handleSubmit"
        >
          <span v-if="submitting">提交中...</span>
          <span v-else>提交反馈</span>
        </button>
      </div>
    </div>

    <!-- 成功提示弹窗 -->
    <div v-if="showSuccess" class="success-modal">
      <div class="success-content" @click.stop>
        <i class="icon-success"></i>
        <h3>反馈提交成功</h3>
        <p>感谢您的反馈，我们会尽快处理</p>
        <button class="confirm-btn" @click="handleSuccessConfirm">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import './styles/FeedBack.css'

import { authAPI } from '@/utils/api';
import { ref, reactive, watch } from 'vue'

// 定义组件Props
interface Props {
  visible: boolean
}

// 定义组件Emits
interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'submitted', data: { content: string; email?: string }): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 反馈表单数据
const feedbackForm = reactive({
  content: '',
  email: '',
})

// 状态管理
const submitting = ref(false)
const showSuccess = ref(false)

// 监听visible变化，确保能正确响应外部控制
watch(
  () => props.visible,
  (newVal) => {
    if (!newVal) {
      // 关闭时重置表单
      resetForm()
    }
  },
)

// 关闭弹窗
const handleClose = () => {
  emit('update:visible', false)
}

// // 点击遮罩层关闭
// const handleMaskClick = () => {
//   handleClose()
// }

// 重置表单
const resetForm = () => {
  feedbackForm.content = ''
  feedbackForm.email = ''
  submitting.value = false
  showSuccess.value = false
}

// 处理提交
const handleSubmit = async () => {
  if (!feedbackForm.content.trim()) {
    return
  }

  submitting.value = true

  try {

    const token = localStorage.getItem('token') || '';
    // 这里调用你的API
    // await submitFeedback(feedbackForm)

    // 模拟API调用
    const response= await authAPI.feedback(token,{
      content: feedbackForm.content,
      email: feedbackForm.email || undefined,
    } );

    // await new Promise((resolve) => setTimeout(resolve, 1500))

    // 提交成功后显示成功提示
    if (response === 'success'){
          showSuccess.value = true
    }



    // 通知父组件提交成功
    emit('submitted', {
      content: feedbackForm.content,
      email: feedbackForm.email || undefined,
    })
  } catch (error) {
    console.error('提交反馈失败:', error)
    // 这里可以添加错误提示
  } finally {
    submitting.value = false
  }
}

// 成功提示确认
const handleSuccessConfirm = () => {
  showSuccess.value = false
  handleClose()
}
</script>

<style scoped>

</style>
