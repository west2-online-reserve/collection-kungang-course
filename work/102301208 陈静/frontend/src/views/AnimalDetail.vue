<template>
  <div>
    <el-card v-if="animal" class="detail-card">
      <div class="detail-header">
        <h2>{{ animal.name }} 的详细信息</h2>
        <div>
          <el-tag v-if="authStore.isAdmin" type="danger" size="large">管理员</el-tag>
          <el-tag v-else type="info" size="large">普通用户</el-tag>
        </div>
      </div>
      
      <el-descriptions :column="2" border style="margin-top: 20px">
        <el-descriptions-item label="昵称" :span="2">
          <strong style="font-size: 16px">{{ animal.name }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="物种">{{ animal.species }}</el-descriptions-item>
        <el-descriptions-item label="区域">{{ animal.zone }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(animal.status)" size="large">{{ animal.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="绝育状态">
          <el-tag :type="animal.is_sterilized ? 'success' : 'warning'" size="large">
            {{ animal.is_sterilized ? '已绝育' : '未绝育' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发现日期">{{ formatDate(animal.found_date) }}</el-descriptions-item>
        <el-descriptions-item label="录入时间">{{ formatDate(animal.created_at) }}</el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 20px">
        <el-button @click="$router.back()">返回</el-button>
        <el-button type="primary" @click="showEditDialog = true" v-if="authStore.isAdmin">
          编辑信息
        </el-button>
        <el-button type="danger" @click="handleDelete" v-if="authStore.isAdmin">
          删除动物
        </el-button>
        <el-button type="success" @click="applyAdoption" 
                   v-if="animal.status === '流浪中' && !authStore.isAdmin">
          申请领养
        </el-button>
      </div>
    </el-card>
    
    <el-card v-else class="loading-card">
      <el-empty description="暂无数据" />
    </el-card>

    <el-card style="margin-top: 20px" v-if="authStore.isAdmin && feedRecords.length > 0">
      <h3>投喂记录</h3>
      <el-table :data="feedRecords" style="width: 100%" stripe>
        <el-table-column prop="username" label="投喂人" width="150" />
        <el-table-column prop="feed_time" label="时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.feed_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="food_content" label="食物内容" />
      </el-table>
    </el-card>

    <el-card style="margin-top: 20px" v-if="authStore.isAdmin && healthLogs.length > 0">
      <h3>医疗记录</h3>
      <el-table :data="healthLogs" style="width: 100%" stripe>
        <el-table-column prop="action_type" label="类型" width="120" />
        <el-table-column prop="cost" label="费用(元)" width="120" />
        <el-table-column prop="log_date" label="日期" width="150">
          <template #default="{ row }">
            {{ formatDate(row.log_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
      </el-table>
    </el-card>

    <el-card style="margin-top: 20px">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
        <h3>动物相册</h3>
        <el-button type="primary" @click="showPhotoDialog = true" size="small">
          上传照片
        </el-button>
      </div>
      
      <el-empty v-if="photos.length === 0" description="暂无数据" />
      
      <div v-else class="photo-gallery">
        <div v-for="photo in photos" :key="photo.photo_id" class="photo-item">
          <el-image 
            :src="photo.photo_url" 
            :preview-src-list="photos.map(p => p.photo_url)"
            fit="cover"
            class="photo-image">
            <template #error>
              <div class="image-error">
                <el-icon><Picture /></el-icon>
                <span>加载失败</span>
              </div>
            </template>
          </el-image>
          <div class="photo-info">
            <div class="photo-desc">{{ photo.description || '无描述' }}</div>
            <div class="photo-meta">
              <span>{{ photo.username }}</span>
              <span>{{ formatDate(photo.created_at) }}</span>
            </div>
            <el-button 
              v-if="authStore.user.user_id === photo.user_id || authStore.isAdmin"
              type="danger" 
              size="small" 
              @click="deletePhoto(photo.photo_id)"
              style="margin-top: 5px; width: 100%">
              删除
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <el-dialog v-model="showPhotoDialog" title="上传照片" width="500px">
      <el-form :model="photoForm" label-width="100px">
        <el-form-item label="照片URL">
          <el-input v-model="photoForm.photo_url" placeholder="请输入图片URL" />
          <div style="margin-top: 5px; font-size: 12px; color: #909399">
            提示：请输入图片的网络地址，如 https://example.com/image.jpg
          </div>
        </el-form-item>
        <el-form-item label="照片描述">
          <el-input v-model="photoForm.description" type="textarea" :rows="3" 
                    placeholder="可选，描述这张照片" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPhotoDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUploadPhoto">上传</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showEditDialog" title="编辑动物信息" width="500px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="昵称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="物种">
          <el-select v-model="editForm.species" style="width: 100%">
            <el-option label="猫" value="猫" />
            <el-option label="狗" value="狗" />
          </el-select>
        </el-form-item>
        <el-form-item label="区域">
          <el-select v-model="editForm.zone" style="width: 100%">
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
          <el-date-picker v-model="editForm.found_date" type="date" placeholder="选择日期" 
                          format="YYYY/MM/DD" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="editForm.status" style="width: 100%">
            <el-option label="流浪中" value="流浪中" />
            <el-option label="已领养" value="已领养" />
            <el-option label="住院治疗" value="住院治疗" />
            <el-option label="已死亡" value="已死亡" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否绝育">
          <el-switch v-model="editForm.is_sterilized" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUpdate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from '../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const animal = ref(null)
const feedRecords = ref([])
const healthLogs = ref([])
const photos = ref([])
const showEditDialog = ref(false)
const showPhotoDialog = ref(false)
const editForm = ref({})
const photoForm = ref({ photo_url: '', description: '' })

const loadAnimal = async () => {
  const response = await axios.get(`/api/animals/${route.params.id}`)
  animal.value = response.data
  editForm.value = { ...response.data }
}

const loadFeedRecords = async () => {
  const response = await axios.get('/api/feed-records', {
    params: { animal_id: route.params.id }
  })
  feedRecords.value = response.data
}

const loadHealthLogs = async () => {
  const response = await axios.get('/api/health-logs', {
    params: { animal_id: route.params.id }
  })
  healthLogs.value = response.data
}

const loadPhotos = async () => {
  const response = await axios.get(`/api/animals/${route.params.id}/photos`)
  photos.value = response.data
}

const handleUploadPhoto = async () => {
  if (!photoForm.value.photo_url) {
    ElMessage.warning('请输入照片URL')
    return
  }
  
  try {
    await axios.post(`/api/animals/${route.params.id}/photos`, photoForm.value)
    ElMessage.success('照片上传成功')
    showPhotoDialog.value = false
    photoForm.value = { photo_url: '', description: '' }
    loadPhotos()
  } catch (error) {
    ElMessage.error('上传失败')
  }
}

const deletePhoto = async (photoId) => {
  try {
    await ElMessageBox.confirm('确定要删除这张照片吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/photos/${photoId}`)
    ElMessage.success('删除成功')
    loadPhotos()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getStatusType = (status) => {
  const types = { '流浪中': 'warning', '已领养': 'success', '住院治疗': 'danger', '已死亡': 'info' }
  return types[status] || 'info'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${year}/${month}/${day}`
}

const handleUpdate = async () => {
  try {
    await axios.put(`/api/animals/${route.params.id}`, editForm.value)
    ElMessage.success('更新成功')
    showEditDialog.value = false
    loadAnimal()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const applyAdoption = () => {
  router.push({ name: 'Adoptions', query: { animalId: animal.value.animal_id } })
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除动物 "${animal.value.name}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    await axios.delete(`/api/animals/${animal.value.animal_id}`)
    ElMessage.success('删除成功')
    router.push('/animals')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadAnimal()
  loadPhotos()
  if (authStore.isAdmin) {
    loadFeedRecords()
    loadHealthLogs()
  }
})
</script>

<style scoped>
.detail-card {
  margin-bottom: 20px;
}
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.loading-card {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.photo-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
.photo-item {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s;
}
.photo-item:hover {
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}
.photo-image {
  width: 100%;
  height: 200px;
  cursor: pointer;
}
.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  background-color: #f5f7fa;
  color: #909399;
}
.photo-info {
  padding: 10px;
  background-color: #fff;
}
.photo-desc {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.photo-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}
</style>
