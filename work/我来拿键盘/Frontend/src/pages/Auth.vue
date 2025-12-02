<template>
  <div
    class="lg:h-screen min-h-screen bg-parchment flex items-center justify-center lg:overflow-hidden overflow-y-auto py-4 md:py-0 px-3"
  >
    <!-- 背景图 -->
    <div
      class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1529590003495-2e0a378906d1?q=80&w=1920&auto=format&fit=crop')] bg-center bg-cover opacity-40"
    ></div>

    <!-- 主容器：控制布局切换 -->
    <div :class="containerClass">
      <!-- 左侧校史标题容器 -->
      <div :class="leftClass">
        <div class="text-center space-y-4">
          <div
            class="text-4xl md:text-5xl font-serif tracking-wide opacity-0 translate-y-4 animate-text-up"
          >
            福大数字校史
          </div>
          <div
            class="text-lg md:text-xl font-serif opacity-0 translate-y-4 animate-text-up delay-150"
          >
            三维互动叙事 · 历史与文化
          </div>
          <div class="mt-6 flex items-center justify-center">
            <div
              class="w-64 h-40 md:w-80 md:h-52 bg-white/60 border border-white/70 shadow-lg rounded-xl opacity-0 scale-95 animate-text-up delay-300"
            ></div>
          </div>
        </div>
      </div>

      <!-- 右侧登录/注册容器 -->
      <div :class="rightClass">
        <div class="flex items-center justify-between">
          <div class="text-2xl font-semibold">欢迎</div>
          <div class="text-sm text-gray-500">历史感 · 高级感</div>
        </div>

        <!-- 标签切换 -->
        <div class="mt-6 grid grid-cols-2 bg-black/5 rounded-xl overflow-hidden">
          <button :class="tab === 'login' ? activeTab : inactiveTab" @click="tab = 'login'">
            登录
          </button>
          <button :class="tab === 'register' ? activeTab : inactiveTab" @click="tab = 'register'">
            注册
          </button>
        </div>

        <!-- 消息提示 -->
        <div
          v-if="error || success"
          class="mt-4 px-4 py-3 rounded-xl text-white transition-all duration-300 animate-message-fade-in"
          :class="error ? 'bg-red-500' : 'bg-green-500'"
        >
          {{ error || success }}
        </div>

        <!-- 表单容器 -->
        <div class="mt-4 relative">
          <!-- 登录表单组件 -->
          <LoginForm
            v-if="tab === 'login'"
            :loading="loading"
            :errors="loginErrors"
            @login="handleLogin"
          />

          <!-- 注册表单组件 -->
          <RegisterForm
            v-else
            :loading="loading"
            :errors="registerErrors"
            @register="handleRegister"
          />
        </div>
      </div>
    </div>

    <!-- 引入 Font Awesome 图标库 CDN -->
    <link
      rel="stylesheet"
      href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.5.1/css/all.min.css"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'
import LoginForm from '@/components/auth/LoginForm.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'

// 检测移动端
const isMobile = ref(false)

onMounted(() => {
  const updateMobile = () => {
    isMobile.value = window.matchMedia('(max-width: 768px)').matches
  }
  updateMobile()
  window.addEventListener('resize', updateMobile)
})

// 登录/注册标签切换
const tab = ref<'login' | 'register'>('login')
const activeTab = 'py-3 font-medium bg-black text-white transition-colors duration-300'
const inactiveTab = 'py-3 font-medium text-black hover:bg-black/5 transition-colors duration-300'

const containerClass = computed(() => 'relative w-full max-w-6xl h-[620px]')

const leftBaseCommon =
  'h-[620px] min-w-[320px] rounded-2xl backdrop-blur-md bg-white/40 shadow-2xl border border-white/60 flex items-center justify-center select-none z-10 will-change-transform absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'
const rightBaseCommon =
  'h-[620px] min-w-[320px] rounded-2xl bg-white/90 shadow-xl border border-black/5 p-6 md:p-8 z-5 will-change-transform absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'
const widthAnim = 'w-[calc(50%-0.75rem)]'

const leftClass = computed(() => {
  // 移动端：封面逐渐消失
  if (isMobile.value) {
    return `${leftBaseCommon} w-full max-w-md animate-mobile-cover-fade`
  }
  // 桌面端：原有的滑入分离动画
  return `${leftBaseCommon} ${widthAnim} animate-slide-up-left`
})

const rightClass = computed(() => {
  // 移动端：简单的从下方滑入
  if (isMobile.value) {
    return `${rightBaseCommon} w-full max-w-md animate-mobile-form-slide`
  }
  // 桌面端：原有的滑入分离动画
  return `${rightBaseCommon} ${widthAnim} animate-slide-up-right`
})

// 状态管理
const loading = ref(false)
const error = ref('')
const success = ref('')
const router = useRouter()

// 字段级错误状态
const loginErrors = ref({
  studentId: '',
  password: '',
  general: '',
})

const registerErrors = ref({
  studentId: '',
  name: '',
  password: '',
  confirmPassword: '',
  general: '',
})

// 显示全局消息
function showMessage(type: string, message: string) {
  if (type === 'error') {
    error.value = message
    success.value = ''
    // 清除所有字段级错误
    clearFieldErrors()
  } else if (type === 'success') {
    success.value = message
    error.value = ''
    // 成功时清除字段错误
    clearFieldErrors()
  }
  // 3秒后自动清除全局消息
  setTimeout(() => {
    error.value = ''
    success.value = ''
  }, 3000)
}

// 清除字段级错误
function clearFieldErrors() {
  // 明确清除每个字段的错误，避免类型错误
  loginErrors.value.studentId = ''
  loginErrors.value.password = ''
  loginErrors.value.general = ''

  registerErrors.value.studentId = ''
  registerErrors.value.name = ''
  registerErrors.value.password = ''
  registerErrors.value.confirmPassword = ''
  registerErrors.value.general = ''
}

// 显示登录字段级错误
function showLoginFieldError(field: string, message: string) {
  // 清除全局错误，只显示字段错误
  error.value = ''
  // 确保field是有效的键类型
  if (['studentId', 'password', 'general'].includes(field)) {
    loginErrors.value[field as keyof typeof loginErrors.value] = message
  }

  // 5秒后自动清除字段错误
  setTimeout(() => {
    // 确保field是有效的键类型
    if (['studentId', 'password', 'general'].includes(field)) {
      loginErrors.value[field as keyof typeof loginErrors.value] = ''
    }
  }, 5000)
}

// 显示注册字段级错误
function showRegisterFieldError(field: string, message: string) {
  // 清除全局错误，只显示字段错误
  error.value = ''
  // 确保field是有效的键类型
  if (['studentId', 'name', 'password', 'confirmPassword', 'general'].includes(field)) {
    registerErrors.value[field as keyof typeof registerErrors.value] = message
  }

  // 5秒后自动清除字段错误
  setTimeout(() => {
    // 确保field是有效的键类型
    if (['studentId', 'name', 'password', 'confirmPassword', 'general'].includes(field)) {
      registerErrors.value[field as keyof typeof registerErrors.value] = ''
    }
  }, 5000)
}

// 处理登录
const handleLogin = async (loginData: { studentId: string; password: string }) => {
  // 清除之前的错误
  clearFieldErrors()

  // 表单验证 - 使用字段级错误提示
  let hasErrors = false

  if (!loginData.studentId) {
    showLoginFieldError('studentId', '请输入学号')
    hasErrors = true
  } else if (loginData.studentId.length !== 9) {
    showLoginFieldError('studentId', '学号长度必须为9位')
    hasErrors = true
  }

  if (!loginData.password) {
    showLoginFieldError('password', '请输入密码')
    hasErrors = true
  } else if (loginData.password.length < 6) {
    showLoginFieldError('password', '密码长度至少为6位')
    hasErrors = true
  }

  if (hasErrors) {
    return
  }

  loading.value = true

  try {
    const response = await fetch(getApiUrl(API_ENDPOINTS.LOGIN), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })

    const data = await response.json()

    if (response.ok && data.success) {
      localStorage.setItem('token', data.token)
      showMessage('success', '登录成功！')
      router.push('/home')
    } else {
      // 根据不同错误类型提供更具体的中文提示
      let errorMessage = data.message || '登录失败，请检查学号和密码'
      let errorType = 'general' // 默认是一般错误

      // 映射可能的英文错误信息为中文，并分类
      if (errorMessage.toLowerCase().includes('not found')) {
        errorMessage = '该学号未注册'
        errorType = 'studentId'
      } else if (errorMessage.toLowerCase().includes('invalid credentials')) {
        errorMessage = '学号或密码错误'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('invalid password')) {
        errorMessage = '密码错误，请重新输入'
        errorType = 'password'
      } else if (errorMessage.toLowerCase().includes('account locked')) {
        errorMessage = '账户已被锁定，请联系管理员'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('error')) {
        errorMessage = '登录出错，请稍后重试'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('failed')) {
        errorMessage = '登录失败，请检查您的信息'
        errorType = 'general'
      }

      // 根据错误类型显示不同位置的错误
      if (errorType === 'general') {
        showMessage('error', errorMessage)
      } else {
        showLoginFieldError(errorType, errorMessage)
      }
    }
  } catch (err) {
    console.error('登录请求失败:', err)
    showMessage('error', '网络连接失败，请检查网络设置或稍后重试')
  } finally {
    loading.value = false
  }
}

// 处理注册
const handleRegister = async (registerData: {
  studentId: string
  name: string
  password: string
  confirmPassword: string
}) => {
  // 清除之前的错误
  clearFieldErrors()

  // 表单验证 - 使用字段级错误提示
  let hasErrors = false

  if (!registerData.studentId) {
    showRegisterFieldError('studentId', '请输入学号')
    hasErrors = true
  } else if (registerData.studentId.length !== 9) {
    showRegisterFieldError('studentId', '学号长度必须为9位')
    hasErrors = true
  }

  if (!registerData.name) {
    showRegisterFieldError('name', '请输入姓名')
    hasErrors = true
  } else if (registerData.name.length < 2) {
    showRegisterFieldError('name', '姓名长度至少为2个字符')
    hasErrors = true
  }

  if (!registerData.password) {
    showRegisterFieldError('password', '请输入密码')
    hasErrors = true
  } else if (registerData.password.length < 6) {
    showRegisterFieldError('password', '密码长度至少为6位')
    hasErrors = true
  } else if (!/^[a-zA-Z0-9_]+$/.test(registerData.password)) {
    showRegisterFieldError('password', '密码只能包含字母、数字和下划线')
    hasErrors = true
  }

  if (!registerData.confirmPassword) {
    showRegisterFieldError('confirmPassword', '请确认密码')
    hasErrors = true
  } else if (registerData.password !== registerData.confirmPassword) {
    showRegisterFieldError('confirmPassword', '两次输入的密码不一致')
    hasErrors = true
  }

  if (hasErrors) {
    return
  }

  loading.value = true

  try {
    // 创建不包含确认密码的请求数据
    const requestData = {
      studentId: registerData.studentId,
      name: registerData.name,
      password: registerData.password,
    }

    const response = await fetch(getApiUrl(API_ENDPOINTS.REGISTER), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })

    const data = await response.json()

    if (response.ok && data.success) {
      showMessage('success', '注册成功！请登录')
      // 注册成功后切换到登录标签
      tab.value = 'login'
    } else {
      // 根据不同错误类型提供更具体的中文提示
      let errorMessage = data.message || '注册失败，请检查您的信息'
      let errorType = 'general' // 默认是一般错误

      // 映射可能的英文错误信息为中文，并分类
      if (errorMessage.toLowerCase().includes('already exists')) {
        errorMessage = '该学号已被注册'
        errorType = 'studentId'
      } else if (errorMessage.toLowerCase().includes('error')) {
        errorMessage = '注册出错，请稍后重试'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('failed')) {
        errorMessage = '注册失败，请检查您的信息'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('password')) {
        errorMessage = '密码不符合要求，请重新设置'
        errorType = 'password'
      } else if (errorMessage.toLowerCase().includes('length')) {
        errorMessage = '输入长度不符合要求'
        errorType = 'general'
      } else if (errorMessage.toLowerCase().includes('name')) {
        errorMessage = '姓名格式不正确'
        errorType = 'name'
      } else if (errorMessage.toLowerCase().includes('invalid')) {
        errorMessage = '输入信息无效，请检查后重试'
        errorType = 'general'
      }

      // 根据错误类型显示不同位置的错误
      if (errorType === 'general') {
        showMessage('error', errorMessage)
      } else {
        showRegisterFieldError(errorType, errorMessage)
      }
    }
  } catch (err) {
    console.error('注册请求失败:', err)
    showMessage('error', '网络连接失败，请检查网络设置或稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 修改动画样式，实现两个面板自中线底部滑入后再分离 */
@keyframes slideUpLeft {
  0% {
    opacity: 0;
    transform: translate(-50%, 120%);
  }
  45% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  100% {
    opacity: 1;
    transform: translate(calc(-50% - 50% - 1rem), -50%);
  }
}

@keyframes slideUpRight {
  0% {
    opacity: 0;
    transform: translate(-50%, 120%);
  }
  45% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  100% {
    opacity: 1;
    transform: translate(calc(-50% + 50% + 1rem), -50%);
  }
}

/* 移动端动画：封面从下方滑入后逐渐消失 */
@keyframes mobileCoverFade {
  0% {
    opacity: 0;
    transform: translate(-50%, 120%);
  }
  45% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  70% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }
}

/* 移动端动画：表单从下方滑入并保持 */
@keyframes mobileFormSlide {
  0% {
    opacity: 0;
    transform: translate(-50%, 120%);
  }
  45% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

@keyframes simpleFadeUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes formFadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 动画类 */
.animate-slide-up-left {
  animation: slideUpLeft 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-slide-up-right {
  animation: slideUpRight 1.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-mobile-cover-fade {
  animation: mobileCoverFade 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-mobile-form-slide {
  animation: mobileFormSlide 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.animate-text-up {
  animation: simpleFadeUp 0.8s ease-out forwards;
}
.animate-form-fade-in {
  animation: formFadeIn 0.5s ease-out forwards;
  animation-delay: 0.3s;
}
/* 延迟类 */
.delay-150 {
  animation-delay: 0.15s;
}
.delay-300 {
  animation-delay: 0.3s;
}

/* 消息淡入动画 */
@keyframes messageFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-message-fade-in {
  animation: messageFadeIn 0.3s ease-out forwards;
}

/* 移动端遮罩淡入动画 */
@keyframes mobileWarning {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-mobile-warning {
  animation: mobileWarning 0.35s ease-out forwards;
}

/* 优化 Font Awesome 图标样式 */
:deep(.fa-fw) {
  font-size: 16px; /* 匹配输入框文字大小 */
  line-height: 1; /* 垂直居中 */
}

/* 错误消息淡入动画 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.will-change-transform {
  will-change: transform;
}
</style>
