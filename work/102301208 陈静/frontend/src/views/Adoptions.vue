<template>
  <div>
    <el-card>
      <div class="header-actions">
        <h2>领养申请管理</h2>
        <div class="header-right">
          <el-tag v-if="authStore.isAdmin" type="danger" size="large">管理员</el-tag>
          <el-tag v-else type="info" size="large">普通用户</el-tag>
          <el-button type="primary" @click="showDialog = true" v-if="!authStore.isAdmin" style="margin-left: 10px">
            提交申请
          </el-button>
        </div>
      </div>

      <el-empty v-if="applications.length === 0" description="暂无数据" />
      
      <el-table v-else :data="applications" style="width: 100%" stripe>
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="animal_name" label="动物" />
        <el-table-column prop="username" label="申请人" v-if="authStore.isAdmin" />
        <el-table-column prop="apply_reason" label="申请理由" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="申请时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" v-if="authStore.isAdmin">
          <template #default="{ row }">
            <el-button size="small" type="success" @click="handleApprove(row, '已通过')"
                       v-if="row.status === '待审核'">
              通过
            </el-button>
            <el-button size="small" type="danger" @click="handleApprove(row, '已驳回')"
                       v-if="row.status === '待审核'">
              驳回
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" title="提交领养申请" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择动物">
          <el-select v-model="form.animal_id" placeholder="请选择动物" filterable>
            <el-option v-for="animal in availableAnimals" :key="animal.animal_id" 
                       :label="animal.name" :value="animal.animal_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="申请理由">
          <el-input v-model="form.apply_reason" type="textarea" :rows="4" 
                    placeholder="请描述您的养宠经验、居住环境等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from '../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const authStore = useAuthStore()
const applications = ref([])
const availableAnimals = ref([])
const showDialog = ref(false)
const form = ref({ animal_id: null, apply_reason: '' })

const loadApplications = async () => {
  const response = await axios.get('/api/adoptions')
  // 按申请时间降序排序，最新的在前
  applications.value = response.data.sort((a, b) => {
    return new Date(b.create_time) - new Date(a.create_time)
  })
}

const loadAvailableAnimals = async () => {
  const response = await axios.get('/api/animals', { params: { status: '流浪中' } })
  availableAnimals.value = response.data
}

const getStatusType = (status) => {
  const types = { '待审核': 'warning', '已通过': 'success', '已驳回': 'danger' }
  return types[status] || 'info'
}

const formatDate = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${year}/${month}/${day}`
}

const handleCreate = async () => {
  if (!form.value.animal_id) {
    ElMessage.warning('请选择要领养的动物')
    return
  }
  if (!form.value.apply_reason || form.value.apply_reason.trim() === '') {
    ElMessage.warning('请填写申请理由')
    return
  }
  
  // 检查是否已经申请过该动物
  const existingApp = applications.value.find(
    app => app.animal_id === form.value.animal_id && app.status === '待审核'
  )
  if (existingApp) {
    ElMessage.warning('您已经提交过该动物的领养申请，请等待审核')
    return
  }
  
  try {
    await axios.post('/api/adoptions', form.value)
    ElMessage.success('申请已提交')
    showDialog.value = false
    form.value = { animal_id: null, apply_reason: '' }
    loadApplications()
  } catch (error) {
    const msg = error.response?.data?.message || '提交失败'
    ElMessage.error(msg)
  }
}

const handleApprove = async (row, status) => {
  try {
    await ElMessageBox.confirm(`确定要${status === '已通过' ? '通过' : '驳回'}该申请吗？`, '提示')
    await axios.put(`/api/adoptions/${row.application_id}/approve`, { status })
    ElMessage.success('操作成功')
    loadApplications()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  loadApplications()
  if (!authStore.isAdmin) {
    loadAvailableAnimals()
    if (route.query.animalId) {
      form.value.animal_id = parseInt(route.query.animalId)
      showDialog.value = true
    }
  }
})
</script>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
