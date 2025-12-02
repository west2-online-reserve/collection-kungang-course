<template>
  <form
    @submit.prevent="onLogin"
    class="space-y-4 opacity-0 translate-y-2 animate-form-fade-in absolute w-full top-0"
  >
    <div class="space-y-2">
      <label class="text-sm text-gray-700">学号</label>
      <input
        v-model="login.studentId"
        type="text"
        maxlength="9"
        :class="[
          'w-full px-4 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
          loginErrors.studentId
            ? 'border-red-500 focus:ring-red-200'
            : 'border focus:ring-black/10',
        ]"
        placeholder="学号"
      />
      <div v-if="loginErrors.studentId" class="text-red-500 text-xs mt-1 animate-fade-in">
        <i class="fa-solid fa-circle-exclamation mr-1"></i>{{ loginErrors.studentId }}
      </div>
    </div>
    <div class="space-y-2">
      <label class="text-sm text-gray-700">密码</label>
      <div class="relative">
        <input
          v-model="login.password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="current-password"
          :class="[
            'w-full pl-4 pr-12 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
            loginErrors.password
              ? 'border-red-500 focus:ring-red-200'
              : 'border focus:ring-black/10',
          ]"
          placeholder="密码"
        />
        <!-- 替换为 Font Awesome 眼睛/闭眼图标 -->
        <button
          type="button"
          @click="togglePasswordVisibility"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none transition-colors"
          aria-label="切换密码可见性"
        >
          <i
            class="fa-fw"
            :class="showPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
          ></i>
        </button>
      </div>
      <div v-if="loginErrors.password" class="text-red-500 text-xs mt-1 animate-fade-in">
        <i class="fa-solid fa-circle-exclamation mr-1"></i>{{ loginErrors.password }}
      </div>
    </div>
    <button
      type="submit"
      :disabled="loading"
      class="w-full py-3 rounded-xl bg-black text-white hover:bg-black/90 transition disabled:opacity-70 disabled:cursor-not-allowed"
    >
      {{ loading ? '登录中...' : '登录' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, defineProps, defineEmits } from 'vue'

// 定义Props
const props = defineProps<{
  loading: boolean
}>()

// 定义Emits
const emit = defineEmits(['login', 'showError', 'clearErrors'])

// 表单数据
const login = reactive({ studentId: '', password: '' })

// 密码可见性状态
const showPassword = ref(false)

// 错误状态
const loginErrors = reactive({
  studentId: '',
  password: '',
  general: ''
})

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// 登录提交
const onLogin = async () => {
  // 清除之前的错误
  emit('clearErrors')

  // 重置本地错误状态
  loginErrors.studentId = ''
  loginErrors.password = ''

  // 表单验证 - 使用字段级错误提示
  let hasErrors = false

  if (!login.studentId) {
    emit('showError', 'studentId', '请输入学号')
    hasErrors = true
  } else if (login.studentId.length !== 9) {
    emit('showError', 'studentId', '学号长度必须为9位')
    hasErrors = true
  }

  if (!login.password) {
    emit('showError', 'password', '请输入密码')
    hasErrors = true
  } else if (login.password.length < 6) {
    emit('showError', 'password', '密码长度至少为6位')
    hasErrors = true
  }

  if (hasErrors) {
    return
  }

  // 向父组件发送登录数据
  emit('login', { ...login })
}
</script>

<style scoped>
/* 表单淡入动画 */
@keyframes formFadeIn {
  from {
    opacity: 0;
    transform: translateY(2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-form-fade-in {
  animation: formFadeIn 0.3s ease-out forwards;
}

/* 错误提示淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>
