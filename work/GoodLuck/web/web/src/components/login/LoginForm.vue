<template>
  <div class="form-card">
    <h2 class="form-title">
      <i class="fa fa-leaf form-icon"></i>运动数据管理
    </h2>
    <h5 class="text-center text-muted mb-4">欢迎登录 {{ title  }}</h5>

    <div v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="mb-4 d-flex align-items-center">
        <label for="login-username" class="form-label me-3 mb-0" style="font-weight: 600; width: 80px;">用户名</label>
        <div class="input-group flex-grow-1">

          <input
            type="text"
            data-lpignore="true"
            class="form-control"
            id="login-username"
            v-model="formData.username"
            placeholder="请输入用户名（至少3位）"
            required>
        </div>
      </div>

      <div class="mb-4 d-flex align-items-center">
        <label for="login-password" class="form-label me-3 mb-0" style="font-weight: 600; width: 80px;">密码</label>
        <div class="input-group">

          <input
            type="password"
            data-lpignore="true"
            class="form-control"
            id="login-password"
            v-model="formData.password"
            placeholder="请输入密码（至少6位）"
            required>
        </div>
      </div>

      <!-- <div class="form-check mb-4">
        <input type="checkbox" class="form-check-input" id="remember-me" v-model="rememberMe">
        <label class="form-check-label" for="remember-me" >记住我</label>
      </div> -->

      <button type="submit" class="btn btn-sports w-100" :disabled="loading">
        <i class="fa fa-sign-in mr-2"></i>
        {{ loading ? '登录中...' : '登录' }}
      </button>

      <div class="text-center mt-3">
        <span>还没有账号？</span>
        <a href="javascript:;" class="link-sports" @click="$emit('switch-to-register')">立即注册</a>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { LoginData } from '@/types/auth';
import { authAPI } from '@/utils/api';

const title = import.meta.env.VITE_TITLE ;

interface Emits {
  (e: 'switch-to-register'): void;
  (e: 'login-success'): void;
}

const emit = defineEmits<Emits>();

const formData = reactive<LoginData>({
  username: '',
  password: ''
});

const loading = ref(false);
const errorMessage = ref('');



const validateForm = (): boolean => {
  if (!formData.username.trim() || !formData.password.trim()) {
    errorMessage.value = '用户名和密码不能为空！';
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

  return true;
};


const handleSubmit = async () => {
  errorMessage.value = '';

  if (!validateForm()) {
    return;
  }

  loading.value = true;

  try {
    const response = await authAPI.login(formData);

    if (response.code === 200) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('role', JSON.stringify(response.data.user.role));


      // alert('登录成功！即将进入系统');
      emit('login-success');
    } else  {
      console.log(response)
      errorMessage.value = response.message || '登录失败！';
    }
  } catch (error) {
    console.error('登录错误:', error);
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

.form-check-label {
    display: block;
    text-align: left;
    width: 100%;
    font-size: medium;
    margin-left: 8px;
}
</style>
