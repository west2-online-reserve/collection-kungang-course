<template>
  <div>
    <el-card>
      <div class="header-actions">
        <h2>医疗记录管理</h2>
        <div class="header-right">
          <el-tag type="danger" size="large">管理员</el-tag>
          <el-button type="primary" @click="showDialog = true" style="margin-left: 10px">添加记录</el-button>
        </div>
      </div>

      <el-empty v-if="logs.length === 0" description="暂无数据" />
      
      <el-table v-else :data="logs" style="width: 100%" stripe>
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="animal_name" label="动物" />
        <el-table-column prop="action_type" label="类型" />
        <el-table-column prop="cost" label="费用(元)" />
        <el-table-column prop="log_date" label="日期">
          <template #default="{ row }">
            {{ formatDate(row.log_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" title="添加医疗记录" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择动物">
          <el-select v-model="form.animal_id" placeholder="请选择动物" filterable>
            <el-option v-for="animal in animals" :key="animal.animal_id" 
                       :label="animal.name" :value="animal.animal_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.action_type" style="width: 100%">
            <el-option label="绝育" value="绝育" />
            <el-option label="疫苗" value="疫苗" />
            <el-option label="治疗" value="治疗" />
            <el-option label="驱虫" value="驱虫" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="form.log_date" type="date" placeholder="选择日期" 
                          format="YYYY/MM/DD" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="费用">
          <el-input-number v-model="form.cost" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../utils/axios'
import { ElMessage } from 'element-plus'

const logs = ref([])
const animals = ref([])
const showDialog = ref(false)
const form = ref({ animal_id: null, action_type: '疫苗', log_date: '', cost: 0, description: '' })

const loadLogs = async () => {
  const response = await axios.get('/api/health-logs')
  // 按日期降序排序，最新的在前
  logs.value = response.data.sort((a, b) => {
    return new Date(b.log_date) - new Date(a.log_date)
  })
}

const loadAnimals = async () => {
  const response = await axios.get('/api/animals')
  animals.value = response.data
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${year}/${month}/${day}`
}

const handleCreate = async () => {
  if (!form.value.animal_id) {
    ElMessage.warning('请选择动物')
    return
  }
  if (!form.value.log_date) {
    ElMessage.warning('请选择日期')
    return
  }
  
  try {
    await axios.post('/api/health-logs', form.value)
    ElMessage.success('添加成功')
    showDialog.value = false
    form.value = { animal_id: null, action_type: '疫苗', log_date: '', cost: 0, description: '' }
    loadLogs()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

onMounted(() => {
  loadLogs()
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
</style>
