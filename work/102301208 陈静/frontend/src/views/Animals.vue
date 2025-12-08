<template>
  <div>
    <el-card>
      <div class="header-actions">
        <h2>动物档案管理</h2>
        <div class="header-right">
          <el-tag v-if="authStore.isAdmin" type="danger" size="large">管理员</el-tag>
          <el-tag v-else type="info" size="large">普通用户</el-tag>
          <el-button type="primary" @click="showDialog = true" v-if="authStore.isAdmin" style="margin-left: 10px">
            添加动物
          </el-button>
        </div>
      </div>
      
      <el-form :inline="true" class="filter-form">
        <el-form-item label="区域">
          <el-select v-model="filters.zone" placeholder="选择区域" clearable style="width: 180px">
            <el-option label="图书馆" value="图书馆" />
            <el-option label="宿舍1区" value="宿舍1区" />
            <el-option label="宿舍2区" value="宿舍2区" />
            <el-option label="宿舍3区" value="宿舍3区" />
            <el-option label="宿舍4区" value="宿舍4区" />
            <el-option label="宿舍5区" value="宿舍5区" />
            <el-option label="东教学楼" value="东教学楼" />
            <el-option label="西教学楼" value="西教学楼" />
            <el-option label="文楼" value="文楼" />
            <el-option label="科技园" value="科技园" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="选择状态" clearable style="width: 180px">
            <el-option label="流浪中" value="流浪中" />
            <el-option label="已领养" value="已领养" />
            <el-option label="住院治疗" value="住院治疗" />
          </el-select>
        </el-form-item>
        <el-form-item label="绝育">
          <el-select v-model="filters.is_sterilized" placeholder="绝育状态" clearable style="width: 180px">
            <el-option label="已绝育" value="true" />
            <el-option label="未绝育" value="false" />
          </el-select>
        </el-form-item>
        <el-button type="primary" @click="loadAnimals">搜索</el-button>
      </el-form>

      <el-empty v-if="animals.length === 0" description="暂无数据" />
      
      <el-table v-else :data="animals" style="width: 100%" stripe>
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="name" label="昵称" />
        <el-table-column prop="species" label="物种" />
        <el-table-column prop="zone" label="区域" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_sterilized" label="绝育">
          <template #default="{ row }">
            <el-tag :type="row.is_sterilized ? 'success' : 'warning'">
              {{ row.is_sterilized ? '已绝育' : '未绝育' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row.animal_id)">详情</el-button>
            <el-button size="small" type="primary" @click="applyAdoption(row)" 
                       v-if="row.status === '流浪中' && !authStore.isAdmin">
              申请领养
            </el-button>
            <el-button size="small" type="danger" @click="deleteAnimal(row)" 
                       v-if="authStore.isAdmin">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" title="添加动物" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="昵称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="物种">
          <el-select v-model="form.species" style="width: 100%">
            <el-option label="猫" value="猫" />
            <el-option label="狗" value="狗" />
          </el-select>
        </el-form-item>
        <el-form-item label="区域">
          <el-select v-model="form.zone" placeholder="请选择区域" style="width: 100%">
            <el-option label="图书馆" value="图书馆" />
            <el-option label="宿舍1区" value="宿舍1区" />
            <el-option label="宿舍2区" value="宿舍2区" />
            <el-option label="宿舍3区" value="宿舍3区" />
            <el-option label="宿舍4区" value="宿舍4区" />
            <el-option label="宿舍5区" value="宿舍5区" />
            <el-option label="东教学楼" value="东教学楼" />
            <el-option label="西教学楼" value="西教学楼" />
            <el-option label="文楼" value="文楼" />
            <el-option label="科技园" value="科技园" />
          </el-select>
        </el-form-item>
        <el-form-item label="发现日期">
          <el-date-picker v-model="form.found_date" type="date" placeholder="选择日期" 
                          format="YYYY/MM/DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="是否绝育">
          <el-switch v-model="form.is_sterilized" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false" :disabled="isSubmitting">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="isSubmitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from '../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const animals = ref([])
const showDialog = ref(false)
const filters = ref({ zone: '', status: '', is_sterilized: '' })
const form = ref({ name: '', species: '猫', zone: '', found_date: '', is_sterilized: false })
const isSubmitting = ref(false)

const loadAnimals = async () => {
  const params = {}
  if (filters.value.zone) params.zone = filters.value.zone
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.is_sterilized) params.is_sterilized = filters.value.is_sterilized
  
  const response = await axios.get('/api/animals', { params })
  animals.value = response.data
}

const getStatusType = (status) => {
  const types = { '流浪中': 'warning', '已领养': 'success', '住院治疗': 'danger', '已死亡': 'info' }
  return types[status] || 'info'
}

const viewDetail = (id) => {
  router.push(`/animals/${id}`)
}

const applyAdoption = (animal) => {
  if (animal.status !== '流浪中') {
    ElMessage.warning('该动物不可领养')
    return
  }
  router.push({ name: 'Adoptions', query: { animalId: animal.animal_id } })
}

const deleteAnimal = async (animal) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除动物 "${animal.name}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    await axios.delete(`/api/animals/${animal.animal_id}`)
    ElMessage.success('删除成功')
    loadAnimals()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleCreate = async () => {
  if (isSubmitting.value) {
    return
  }
  
  if (!form.value.name || !form.value.name.trim()) {
    ElMessage.warning('请输入动物昵称')
    return
  }
  
  if (!form.value.zone || !form.value.zone.trim()) {
    ElMessage.warning('请输入区域')
    return
  }
  
  isSubmitting.value = true
  try {
    await axios.post('/api/animals', form.value)
    ElMessage.success('添加成功')
    showDialog.value = false
    form.value = { name: '', species: '猫', zone: '', found_date: '', is_sterilized: false }
    loadAnimals()
  } catch (error) {
    const msg = error.response?.data?.message || '添加失败'
    ElMessage.error(msg)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadAnimals()
})
</script>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.filter-form {
  margin-bottom: 20px;
}
.filter-form .el-form-item {
  margin-bottom: 0;
}
</style>
