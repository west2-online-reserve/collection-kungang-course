<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <!-- 模态框头部 -->
      <div class="modal-header">
        <h5 class="modal-title">
          <i class="fa fa-lock me-2 text-warning"></i>修改密码
        </h5>
        <button type="button" class="btn-close" @click="close"></button>
      </div>

      <!-- 模态框主体 -->
      <div class="modal-body">
        <form @submit.prevent="submitChangePassword">


          <div class="mb-3">
            <label for="newPassword" class="form-label">新密码</label>
            <input
              type="password"
              class="form-control"
              id="newPassword"
              v-model="passwordForm.newPassword"
              placeholder="请输入新密码"
              :class="{ 'is-invalid': errors.newPassword }"
            >
            <div class="invalid-feedback" v-if="errors.newPassword">
              {{ errors.newPassword }}
            </div>
            <div class="form-text">
              密码长度至少6位
            </div>
          </div>

          <div class="mb-3">
            <label for="confirmPassword" class="form-label">确认新密码</label>
            <input
              type="password"
              class="form-control"
              id="confirmPassword"
              v-model="passwordForm.confirmPassword"
              placeholder="请再次输入新密码"
              :class="{ 'is-invalid': errors.confirmPassword }"
            >
            <div class="invalid-feedback" v-if="errors.confirmPassword">
              {{ errors.confirmPassword }}
            </div>
          </div>
        </form>
      </div>

      <!-- 模态框底部 -->
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-secondary"
          @click="close"
          :disabled="loading"
        >
          取消
        </button>
        <button
          type="button"
          class="btn btn-primary"
          @click="submitChangePassword"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading ? '修改中...' : '确认修改' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { authAPI } from '@/utils/api'
import { showSuccessMessage} from '@/utils/log'
import { AxiosError } from 'axios'

interface PasswordForm {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}

interface Errors {
  currentPassword?: string
  newPassword?: string
  confirmPassword?: string
}

const emit = defineEmits<{
  close: []
  success: []
}>()

const loading = ref(false)
const passwordForm = reactive<PasswordForm>({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const errors = reactive<Errors>({})

// 关闭模态框
const close = () => {
  if (!loading.value) {
    emit('close')
  }
}

// 验证表单
const validateForm = (): boolean => {
  // 清空之前的错误信息
  Object.keys(errors).forEach(key => {
    delete errors[key as keyof Errors]
  })

  let isValid = true



  // 验证新密码
  if (!passwordForm.newPassword.trim()) {
    errors.newPassword = '请输入新密码'
    isValid = false
  } else if (passwordForm.newPassword.length < 6) {
    errors.newPassword = '密码长度至少6位'
    isValid = false
  }

  // 验证确认密码
  if (!passwordForm.confirmPassword.trim()) {
    errors.confirmPassword = '请确认新密码'
    isValid = false
  } else if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致'
    isValid = false
  }

  return isValid
}

// 提交修改密码
const submitChangePassword = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    // 调用修改密码API
    await authAPI.changePassword(
      localStorage.getItem('token') || '',
      passwordForm.newPassword
    )

    // 显示成功消息
    showSuccessMessage('密码修改成功！', 1500)

    // 重置表单
    resetForm()

    // 触发成功事件
    emit('success')

    // 关闭模态框
    emit('close')

  } catch (error: unknown) {
    console.error('修改密码失败:', error)

    // 根据错误信息显示相应的提示
    if (error instanceof AxiosError && error.response?.data?.message) {
      showSuccessMessage(error.response.data.message, 1500)
    } else {
      showSuccessMessage('修改密码失败，请稍后重试', 1500)
    }
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  Object.keys(errors).forEach(key => {
    delete errors[key as keyof Errors]
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 500px;
  animation: modal-appear 0.3s ease-out;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
}

.btn-close {
  border: none;
  background: none;
  font-size: 1.25rem;
  opacity: 0.7;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.btn-close:hover {
  opacity: 1;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.form-text {
  font-size: 0.875rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 576px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
}
</style>
