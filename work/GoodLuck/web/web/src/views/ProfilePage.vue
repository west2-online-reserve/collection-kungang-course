<template>
  <div class="profile-container">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- 页面标题 -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="page-title">个人资料</h2>
          <button class="btn btn-outline-secondary" @click="back">
            <i class="fa fa-arrow-left me-2"></i>返回
          </button>
        </div>

        <!-- 个人信息卡片 -->
        <div class="card shadow-sm">
          <div class="card-header bg-white">
            <h5 class="card-title mb-0">
              <i class="fa fa-user me-2 text-primary"></i>基本信息
            </h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="saveProfile">
              <div class="row">



                <!-- 基本信息表单 -->
                <div class="col-md-9">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label for="username" class="form-label">用户名</label>
                      <input
                        type="text"
                        class="form-control"
                        id="username"
                        v-model="form.username"
                        placeholder="请输入用户名"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="height" class="form-label">身高</label>
                      <input
                        type="height"
                        class="form-control"
                        id="height"
                        v-model="form.height"
                        placeholder="请输身高"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="weight" class="form-label">体重</label>
                      <input
                        type="weight"
                        class="form-control"
                        id="weight"
                        v-model="form.weight"
                        placeholder="请输入体重"
                      >
                    </div>

                  </div>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="row mt-4">
                <div class="col-12">
                  <div class="d-flex gap-2 justify-content-end">
                    <button type="button" class="btn btn-secondary" @click="resetForm">重置</button>
                    <button type="submit" class="btn btn-primary" :disabled="loading">
                      <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                      {{ loading ? '保存中...' : '保存更改' }}
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- 安全设置卡片 -->
        <div class="card shadow-sm mt-4">
          <div class="card-header bg-white">
            <h5 class="card-title mb-0">
              <i class="fa fa-shield me-2 text-warning"></i>安全设置
            </h5>
          </div>
          <div class="card-body">
            <div class="list-group list-group-flush">
              <div class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">修改密码</h6>
                  <p class="mb-0 text-muted small">定期修改密码以保证账户安全</p>
                </div>
                <button class="btn btn-outline-primary btn-sm" @click="showChangePassword = true">
                  修改
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码模态框 -->
    <ChangePasswordModal
      v-if="showChangePassword"
      @close="showChangePassword = false"
      @success="handlePasswordChangeSuccess"
    />


  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/utils/api'
import type {SimpleProfileForm } from '@/types/auth'
import {showSuccessMessage} from '@/utils/log'
import ChangePasswordModal from '@/components/main/features/ChangePasswordModal.vue'



const router = useRouter()
const loading = ref(false)
const showChangePassword = ref(false)


// 表单数据
const form = reactive<SimpleProfileForm>({
  username: '',
  height: '',
  weight: '',

})

// 原始数据用于重置
const originalForm = ref<SimpleProfileForm>({ ...form })



// 加载用户资料
const loadUserProfile = async () => {
  try {
    // 这里调用API获取用户信息
    const response = await authAPI.verifyToken(localStorage.getItem('token') || '')




    Object.assign(form, response)

    Object.assign(originalForm.value, { ...form })
  } catch (error) {
    console.error('加载用户资料失败:', error)
    router.push('/login')
  }
}

await loadUserProfile();

// 保存资料
const saveProfile = async () => {
  loading.value = true
  try {
    // 调用API保存资料
    await authAPI.update_simple_profile( localStorage.getItem('token') || '',form)



    // 更新原始数据
    Object.assign(originalForm.value, { ...form })

    // 显示成功消息
    // 可以使用 toast 或 message 组件
    showSuccessMessage('资料保存成功！',1500)

    console.log('资料保存成功')
  } catch (error) {
    showSuccessMessage('资料保存失败！',1500)
    console.error('保存资料失败:', error)
  } finally {
    loading.value = false
  }
}

const back = () => {
  router.push('/main');
}

// 重置表单
const resetForm = () => {
  Object.assign(form, { ...originalForm.value })
}

// 密码修改成功回调
const handlePasswordChangeSuccess = () => {
  showChangePassword.value = false
  // 可以显示成功消息
  console.log('密码修改成功')
}
</script>

<style scoped>
.profile-container {
  padding: 2rem 0;
}

.page-title {
  color: #2c3e50;
  font-weight: 600;
}

.avatar-section {
  position: relative;
}

.avatar-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border: 3px solid #f8f9fa;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.avatar-upload-btn {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 32px;
  height: 32px;
  background: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  background: #0056b3;
  transform: scale(1.1);
}

.card {
  border: none;
  border-radius: 12px;
}

.card-header {
  border-bottom: 1px solid #e9ecef;
  padding: 1.25rem;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.list-group-item {
  border: none;
  padding: 1.25rem;
}

.list-group-item:not(:last-child) {
  border-bottom: 1px solid #e9ecef !important;
}
</style>
