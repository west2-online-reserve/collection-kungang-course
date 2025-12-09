<template>
  <div class="login">
    <SplashScreen />

    <!-- 背景 -->
    <div class="sports-bg"></div>

    <!-- 主内容 -->
    <div class="container py-5">

      <div class="auth-container">

        <!-- 登录表单 -->
        <LoginForm
          v-if="currentForm === 'login'"
          @switch-to-register="currentForm = 'register'"
          @login-success="handleLoginSuccess" />

        <!-- 注册表单 -->
        <RegisterForm
          v-else
          @switch-to-login="currentForm = 'login'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SplashScreen from '@/components/login/SplashScreen.vue';
import LoginForm from '@/components/login/LoginForm.vue';
import RegisterForm from '@/components/login/RegisterForm.vue';
import { authAPI } from '@/utils/api';
import { showSuccessMessage } from '@/utils/log';
import type { User } from '@/types/auth';
const router = useRouter();
const currentForm = ref<'login' | 'register'>('login');



// 检查是否已登录
const checkAuthStatus = async () => {
  const token = localStorage.getItem('token');

  if (!token) {
    return;
  }

  try {
    const response=await authAPI.verifyToken(token);

    showSuccessMessage('自动登录成功！欢迎回来！',2000);
    await new Promise(resolve => setTimeout(resolve, 500));

    console.log(response.role,response.username)
    if (response.role==='admin'){
      router.push('/admin')
    }else{
          // Token有效，跳转到主页
    router.push('/main');
    }

  } catch (error) {
    console.error('Token验证失败:', error);
    // 清除无效的token
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

const handleLoginSuccess = async() => {
  showSuccessMessage('登录成功！即将进入系统',2000);

  const role:string=JSON.parse(localStorage.getItem('role') || '""')


  await new Promise(resolve => setTimeout(resolve, 500));

  if (role==='admin'){

    router.push('/admin')
  }else{

    router.push('/main');
  }

};

onMounted(() => {
  checkAuthStatus();
});
</script>

<style>

.login{
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background-image: url('@/assets/login_bg_1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
/* 全局样式，保持原有的CSS */
body {
  background: #f0f7ee;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(76, 175, 80, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(76, 175, 80, 0.05) 0%, transparent 20%);
  min-height: 100vh;
  font-family: 'Segoe UI', Roboto, sans-serif;
}

.sports-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/login_bg_1.png');
  background-size: cover;
  background-position: center;
  filter: brightness(0.7) sepia(0.2);
  z-index: -1;
}

.auth-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  padding: 40px;
  width: 100%;

  margin: auto auto;
  border-top: 5px solid #4caf50;
  backdrop-filter: blur(10px);
  overflow: hidden;
  position: relative;
  max-width: 450px;
  text-align: center;
  z-index: 1;
  position: relative;
  animation: fadeInUp 0.8s ease-out;
}

.form-title {
  text-align: center;
  margin-bottom: 30px;
  color: #2e7d32;
  font-weight: 700;
  position: relative;
  font-family: 'Fredoka One', cursive;
  font-size: 2.2rem;
}

.form-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: #4caf50;
  margin: 10px auto;
  border-radius: 3px;
}

.form-icon {
  font-size: 28px;
  color: #4caf50;
  margin-right: 10px;
}

.btn-sports {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  border: none;
  color: white;
  padding: 12px 20px;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: 'Fredoka One', cursive;
}

.btn-sports:hover {
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
}

.btn-sports:active {
  transform: translateY(0);
}

.form-control {
  border: 2px solid #e8f5e9;
  border-radius: 8px;
  padding: 12px 15px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.input-group-text {
  background: #f1f8e9;
  border: 2px solid #e8f5e9;
  border-right: none;
  color: #2e7d32;
}

.link-sports {
  color: #2e7d32;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.link-sports:hover {
  color: #1b5e20;
  text-decoration: underline;
}

@media (max-width: 576px) {
  .auth-container {
    padding: 25px;
    margin: 20px;
  }
}
</style>
