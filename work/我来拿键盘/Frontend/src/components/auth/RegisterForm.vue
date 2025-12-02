<template>
  <form
    @submit.prevent="onRegister"
    class="space-y-4 opacity-0 translate-y-2 animate-form-fade-in absolute w-full top-0"
  >
    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-2">
        <label class="text-sm text-gray-700">学号</label>
        <input
          v-model="register.studentId"
          type="text"
          maxlength="9"
          autocomplete="username"
          :class="[
            'w-full px-4 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
            registerErrors.studentId
              ? 'border-red-500 focus:ring-red-200'
              : 'border focus:ring-black/10',
          ]"
          placeholder="学号"
        />
        <div
          v-if="registerErrors.studentId"
          class="text-red-500 text-xs mt-1 animate-fade-in"
        >
          <i class="fa-solid fa-circle-exclamation mr-1"></i>{{ registerErrors.studentId }}
        </div>
      </div>
      <div class="space-y-2">
        <label class="text-sm text-gray-700">姓名</label>
        <input
          v-model="register.name"
          type="text"
          autocomplete="off"
          :class="[
            'w-full px-4 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
            registerErrors.name
              ? 'border-red-500 focus:ring-red-200'
              : 'border focus:ring-black/10',
          ]"
          placeholder="姓名"
        />
        <div v-if="registerErrors.name" class="text-red-500 text-xs mt-1 animate-fade-in">
          <i class="fa-solid fa-circle-exclamation mr-1"></i>{{ registerErrors.name }}
        </div>
      </div>
    </div>
    <div class="space-y-2">
      <label class="text-sm text-gray-700">密码</label>
      <div class="relative">
        <input
          v-model="register.password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="new-password"
          :class="[
            'w-full pl-4 pr-12 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
            registerErrors.password
              ? 'border-red-500 focus:ring-red-200'
              : 'border focus:ring-black/10',
          ]"
          placeholder="密码 (至少6位，仅限字母、数字和下划线)"
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
      <div v-if="registerErrors.password" class="text-red-500 text-xs mt-1 animate-fade-in">
        <i class="fa-solid fa-circle-exclamation mr-1"></i>{{ registerErrors.password }}
      </div>
    </div>
    <div class="space-y-2">
      <label class="text-sm text-gray-700">确认密码</label>
      <div class="relative">
        <input
          v-model="register.confirmPassword"
          :type="showConfirmPassword ? 'text' : 'password'"
          autocomplete="new-password"
          :class="[
            'w-full pl-4 pr-12 py-3 rounded-xl focus:outline-none focus:ring-2 bg-white text-[16px]',
            registerErrors.confirmPassword
              ? 'border-red-500 focus:ring-red-200'
              : 'border focus:ring-black/10',
          ]"
          placeholder="再次输入密码"
        />
        <!-- 替换为 Font Awesome 眼睛/闭眼图标 -->
        <button
          type="button"
          @click="toggleConfirmPasswordVisibility"
          class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none transition-colors"
          aria-label="切换密码可见性"
        >
          <i
            class="fa-fw"
            :class="showConfirmPassword ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash'"
          ></i>
        </button>
      </div>
      <div
        v-if="registerErrors.confirmPassword"
        class="text-red-500 text-xs mt-1 animate-fade-in"
      >
        <i class="fa-solid fa-circle-exclamation mr-1"></i>
        {{ registerErrors.confirmPassword }}
      </div>
    </div>
    <button
      type="submit"
      :disabled="loading"
      class="w-full py-3 rounded-xl bg-black text-white hover:bg-black/90 transition disabled:opacity-70 disabled:cursor-not-allowed"
    >
      {{ loading ? '注册中...' : '注册' }}
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
const emit = defineEmits(['register', 'showError', 'clearErrors'])

// 表单数据
const register = reactive({
  studentId: '',
  name: '',
  password: '',
  confirmPassword: ''
})

// 密码可见性状态
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// 错误状态
const registerErrors = reactive({
  studentId: '',
  name: '',
  password: '',
  confirmPassword: '',
  general: ''
})

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// 切换确认密码可见性
const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

// 注册提交
const onRegister = async () => {
  // 清除之前的错误
  emit('clearErrors')

  // 重置本地错误状态
  registerErrors.studentId = ''
  registerErrors.name = ''
  registerErrors.password = ''
  registerErrors.confirmPassword = ''

  // 表单验证 - 使用字段级错误提示
  let hasErrors = false

  if (!register.studentId) {
    emit('showError', 'studentId', '请输入学号')
    hasErrors = true
  } else if (register.studentId.length !== 9) {
    emit('showError', 'studentId', '学号长度必须为9位')
    hasErrors = true
  }

  if (!register.name) {
    emit('showError', 'name', '请输入姓名')
    hasErrors = true
  } else if (register.name.length < 2) {
    emit('showError', 'name', '姓名长度至少为2个字符')
    hasErrors = true
  }

  if (!register.password) {
    emit('showError', 'password', '请输入密码')
    hasErrors = true
  } else if (register.password.length < 6) {
    emit('showError', 'password', '密码长度至少为6位')
    hasErrors = true
  } else if (!/^[a-zA-Z0-9_]+$/.test(register.password)) {
    emit('showError', 'password', '密码只能包含字母、数字和下划线')
    hasErrors = true
  }

  if (!register.confirmPassword) {
    emit('showError', 'confirmPassword', '请确认密码')
    hasErrors = true
  } else if (register.password !== register.confirmPassword) {
    emit('showError', 'confirmPassword', '两次输入的密码不一致')
    hasErrors = true
  }

  if (hasErrors) {
    return
  }

  // 向父组件发送注册数据
  emit('register', { ...register })
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
