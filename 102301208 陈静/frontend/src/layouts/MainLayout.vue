<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <div class="logo-container">
        <img src="/logo.png" alt="福州大学校徽" class="school-logo" />
        <div class="logo-text">福大流浪动物管理</div>
      </div>
      <el-menu :default-active="$route.path" router>
        <el-menu-item index="/animals">
          <span>动物档案</span>
        </el-menu-item>
        <el-menu-item index="/feed-records">
          <span>投喂记录</span>
        </el-menu-item>
        <el-menu-item index="/health-logs" v-if="authStore.isAdmin">
          <span>医疗记录</span>
        </el-menu-item>
        <el-menu-item index="/adoptions">
          <span>领养申请</span>
        </el-menu-item>
        <el-menu-item index="/dashboard">
          <span>数据统计</span>
        </el-menu-item>
        <el-menu-item index="/users" v-if="authStore.isAdmin">
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="user-info">
            <span class="welcome-text">欢迎，{{ authStore.user?.username }}</span>
            <el-tag v-if="authStore.isAdmin" type="danger" size="large" style="margin-left: 10px">
              管理员
            </el-tag>
            <el-tag v-else type="info" size="large" style="margin-left: 10px">
              普通用户
            </el-tag>
          </div>
          <el-button @click="handleLogout" type="danger" size="small">退出登录</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}
.el-aside {
  background-color: rgb(102, 117, 134);
  color: #fff;
}
.logo-container {
  background-color: rgb(163, 198, 238);
  padding: 20px 10px;
  text-align: center;
}

.school-logo {
  width: 150px;
  height: 60px;
  object-fit: contain;
  margin: 0 auto 12px;
  display: block;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  line-height: 1.4;
}
.el-menu {
  border: none;
  background-color:rgb(102, 117, 134);
}
.el-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}
.user-info {
  display: flex;
  align-items: center;
}
.welcome-text {
  font-size: 16px;
  font-weight: 500;
}
.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
