<template>
  <div>
    <el-card>
      <div class="header-actions">
        <h2>用户管理</h2>
        <div class="header-right">
          <el-tag type="danger" size="large">管理员</el-tag>
        </div>
      </div>

      <div class="search-bar">
        <el-input 
          v-model="searchText" 
          placeholder="搜索用户名、联系方式或角色" 
          clearable
          class="search-input"
          @input="handleSearch"
          @clear="resetSearch"
          @keyup.enter="handleSearch">
        </el-input>
        <el-button type="primary" @click="handleSearch" icon="Search">搜 索</el-button>
        <el-button @click="resetSearch" icon="Refresh">重 置</el-button>
        <span style="margin-left: 20px; color: #909399; font-size: 14px">
          共 {{ filteredUsers.length }} 个用户
        </span>
      </div>

      <el-empty v-if="filteredUsers.length === 0" description="暂无数据" />
      
      <el-table v-else :data="filteredUsers" style="width: 100%" stripe>
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="username" label="用户名" width="150">
          <template #default="{ row }">
            <strong>{{ row.username }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="row.role === '管理员' ? 'danger' : 'info'">
              {{ row.role }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contact" label="联系方式" width="200" />
        <el-table-column prop="created_at" label="注册时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button 
              v-if="row.user_id !== authStore.user.user_id"
              size="small" 
              :type="row.role === '管理员' ? 'warning' : 'primary'"
              @click="toggleRole(row)">
              {{ row.role === '管理员' ? '设为普通用户' : '设为管理员' }}
            </el-button>
            <el-button 
              v-if="row.user_id !== authStore.user.user_id"
              size="small" 
              type="danger"
              @click="deleteUser(row)">
              删除
            </el-button>
            <el-tag v-else type="success" size="small">当前用户</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from '../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const authStore = useAuthStore()
const users = ref([])
const searchText = ref('')
const filteredUsers = ref([])

const loadUsers = async () => {
  try {
    const response = await axios.get('/api/users')
    users.value = response.data
    filteredUsers.value = response.data
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  }
}

const handleSearch = () => {
  if (!searchText.value.trim()) {
    filteredUsers.value = users.value
    return
  }
  
  const keyword = searchText.value.toLowerCase()
  filteredUsers.value = users.value.filter(user => 
    user.username.toLowerCase().includes(keyword) ||
    user.contact?.toLowerCase().includes(keyword) ||
    user.role.includes(keyword)
  )
}

const resetSearch = () => {
  searchText.value = ''
  filteredUsers.value = users.value
}

const formatDate = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${year}/${month}/${day}`
}

const toggleRole = async (user) => {
  const newRole = user.role === '管理员' ? '普通用户' : '管理员'
  const action = newRole === '管理员' ? '设为管理员' : '降为普通用户'
  
  try {
    await ElMessageBox.confirm(
      `确定要将用户 "${user.username}" ${action}吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await axios.put(`/api/users/${user.user_id}/role`, { role: newRole })
    ElMessage.success('角色更新成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      const msg = error.response?.data?.message || '操作失败'
      ElMessage.error(msg)
    }
  }
}

const deleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    await axios.delete(`/api/users/${user.user_id}`)
    ElMessage.success('用户删除成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      const msg = error.response?.data?.message || '删除失败'
      ElMessage.error(msg)
    }
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.header-right {
  display: flex;
  align-items: center;
}
.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.search-input {
  width: 350px;
}
.search-input :deep(.el-input__wrapper) {
  padding: 8px 15px;
}
.search-input :deep(.el-input__inner) {
  text-align: center;
  font-size: 14px;
}
.search-input :deep(.el-input__inner::placeholder) {
  text-align: center;
}
.search-bar :deep(.el-button) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
}
.search-bar :deep(.el-button .el-icon) {
  margin-right: 4px;
  vertical-align: middle;
}
.search-bar :deep(.el-button span) {
  display: inline-flex;
  align-items: center;
}
</style>
