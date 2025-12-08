<template>
  <div>
    <el-card>
      <div class="header-actions">
        <h2>投喂记录管理</h2>
        <div class="header-right">
          <el-tag v-if="authStore.isAdmin" type="danger" size="large">管理员</el-tag>
          <el-tag v-else type="info" size="large">普通用户</el-tag>
          <el-button type="primary" @click="showDialog = true" style="margin-left: 10px">添加记录</el-button>
        </div>
      </div>

      <el-empty v-if="records.length === 0" description="暂无数据" />
      
      <el-table v-else :data="records" style="width: 100%" stripe>
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="animal_name" label="动物" width="120">
          <template #default="{ row }">
            <strong>{{ row.animal_name }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="投喂人" width="150" />
        <el-table-column prop="feed_time" label="时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.feed_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="food_content" label="食物内容" />
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" title="添加投喂记录" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择动物">
          <el-select v-model="form.animal_id" placeholder="请选择动物" filterable>
            <el-option v-for="animal in animals" :key="animal.animal_id" 
                       :label="animal.name" :value="animal.animal_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="食物内容">
          <el-input v-model="form.food_content" type="textarea" />
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
import { useAuthStore } from '../stores/auth'
import axios from '../utils/axios'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

const records = ref([])
const animals = ref([])
const showDialog = ref(false)
const form = ref({ animal_id: null, food_content: '' })

const loadRecords = async () => {
  const response = await axios.get('/api/feed-records')
  // 按时间降序排序，最新的在前
  records.value = response.data.sort((a, b) => {
    return new Date(b.feed_time) - new Date(a.feed_time)
  })
}

const loadAnimals = async () => {
  const response = await axios.get('/api/animals')
  animals.value = response.data
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
  try {
    await axios.post('/api/feed-records', form.value)
    ElMessage.success('添加成功')
    showDialog.value = false
    form.value = { animal_id: null, food_content: '' }
    loadRecords()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

onMounted(() => {
  loadRecords()
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
