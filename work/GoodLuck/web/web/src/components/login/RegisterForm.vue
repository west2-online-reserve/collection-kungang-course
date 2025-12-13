<template>
  <div class="form-card">
    <h2 class="form-title">
      <i class="fa fa-user-plus form-icon"></i>创建账号
    </h2>
    <h5 class="text-center text-muted mb-4">加入{{ title }} 运动社区</h5>

    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label for="register-username" class="form-label">用户名</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa fa-user"></i>
          </span>
          <input
            type="text"
            class="form-control"
            id="register-username"
            v-model="formData.username"
            placeholder="请输入用户名（至少3位）"
            required>
        </div>
      </div>

      <div class="mb-4">
        <label for="register-password" class="form-label">密码</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa fa-lock"></i>
          </span>
          <input
            type="password"
            class="form-control"
            id="register-password"
            v-model="formData.password"
            placeholder="请输入密码（至少6位）"
            required>
        </div>
      </div>

      <div class="mb-4">
        <label for="register-confirm-password" class="form-label">确认密码</label>
        <div class="input-group">
          <span class="input-group-text">
            <i class="fa fa-lock"></i>
          </span>
          <input
            type="password"
            class="form-control"
            id="register-confirm-password"
            v-model="formData.confirmPassword"
            placeholder="请再次输入密码"
            required>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-4">
          <label for="register-height" class="form-label">身高 (cm)</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fa fa-arrows-v"></i>
            </span>
            <input
              type="number"
              class="form-control"
              id="register-height"
              v-model.number="formData.height"
              placeholder="例如：175">
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <label for="register-weight" class="form-label">体重 (kg)</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fa fa-balance-scale"></i>
            </span>
            <input
              type="number"
              class="form-control"
              id="register-weight"
              v-model.number="formData.weight"
              placeholder="例如：70">
          </div>
        </div>
      </div>

      <button type="submit" class="btn btn-sports w-100" :disabled="loading">
        <i class="fa fa-check mr-2"></i>
        {{ loading ? '注册中...' : '注册' }}
      </button>

      <div class="text-center mt-3">
        <span>已有账号？</span>
        <a href="javascript:;" class="link-sports" @click="$emit('switch-to-login')">返回登录</a>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { RegisterData } from '@/types/auth';
import { authAPI } from '@/utils/api';


const title=import.meta.env.VITE_TITLE ;

interface Emits {
  (e: 'switch-to-login'): void;
}

const emit = defineEmits<Emits>();

const formData = reactive<RegisterData>({
  username: '',
  password: '',
  confirmPassword: '',
  height: null,
  weight: null
});

const loading = ref(false);
const errorMessage = ref('');

const validateForm = (): boolean => {
  if (!formData.username.trim() || !formData.password.trim() || !formData.confirmPassword.trim()) {
    errorMessage.value = '用户名、密码和确认密码不能为空！';
    return false;
  }

  if (formData.username.length < 3) {
    errorMessage.value = '用户名至少3位！';
    return false;
  }

  if (formData.password.length < 6) {
    errorMessage.value = '密码至少6位！';
    return false;
  }

  if (formData.password !== formData.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致！';
    return false;
  }

  if (formData.height && (formData.height < 50 || formData.height > 250)) {
    errorMessage.value = '身高请输入合理范围（50-250cm）！';
    return false;
  }

  if (formData.weight && (formData.weight < 10 || formData.weight > 300)) {
    errorMessage.value = '体重请输入合理范围（10-300kg）！';
    return false;
  }

  return true;
};

const handleSubmit = async () => {
  errorMessage.value = '';

  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    // 移除confirmPassword字段，因为后端不需要
    const {  ...registerData } = formData;

    const response = await authAPI.register(registerData);

    if (response.code === 200) {
      alert('注册成功！请登录');
      emit('switch-to-login');

      // 重置表单
      Object.assign(formData, {
        username: '',
        password: '',
        confirmPassword: '',
        height: null,
        weight: null
      });
    } else {
      errorMessage.value = response.message || '注册失败！';
    }
  } catch (error) {
    console.error('注册错误:', error);
    errorMessage.value = error instanceof Error ? error.message : '服务器错误，请稍后重试';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 保持原有的CSS样式 */
.alert-danger {
  margin-bottom: 1rem;
}
</style>
