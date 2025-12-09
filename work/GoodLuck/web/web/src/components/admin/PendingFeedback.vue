<template>
  <!-- 待处理反馈卡片 -->
  <div class="pending-feedback-card">
    <div class="card-header">
      <div class="header-left">
        <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span class="title">待处理反馈</span>
        <span class="badge">{{ pendingCount }}</span>
      </div>
    </div>

    <!-- 新增：筛选区域 -->
    <div class="filters">
      <div class="filter-group">
        <label>类型筛选:</label>
        <select v-model="selectedType" >
          <option value="">全部类型</option>
          <option v-for="type in uniqueTypes" :key="type" :value="type">{{ type }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>状态筛选:</label>
        <select v-model="selectedStatus">
          <option value="">全部状态</option>
          <option value="待处理">待处理</option>
          <option value="已处理">已处理</option>
        </select>
      </div>
    </div>

    <div class="feedback-list">
      <!-- 反馈列表（若无数据显示空状态） -->
      <div v-if="currentPageData.length > 0" class="feedback-items">
        <div
          class="feedback-item"
          v-for="item in currentPageData"
          :key="item.id"
          @mouseenter="hoveredItem = item.id"
          @mouseleave="hoveredItem = null"
          :class="{ 'processed-item': item.status === '已处理' }"
        >
          <div class="item-time">{{ formatTime(item.time) }}</div>
          <div class="item-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="item-content">
            <div class="content-title">{{ item.content.title }}</div>
            <div class="content-desc">{{ item.content.desc }}</div>
          </div>
          <div class="item-type">
            <span class="type-tag">{{ item.type }}</span>
          </div>
          <div class="item-status" v-if="item.status === '已处理'">
            <span class="status-tag processed-tag">已处理</span>
          </div>
          <div class="item-actions" :class="{ show: hoveredItem === item.id && item.status !== '已处理' }">
            <button class="action-btn process-btn" @click="handleProcess(item)">处理</button>
            <button class="action-btn delete-btn" @click="handleIgnore(item)">忽略</button>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <svg class="empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <div class="empty-text">
          <!-- 新增：根据筛选状态显示不同文本 -->
          {{ filteredFeedbackList.length > 0 ? '暂无更多反馈' : '暂无符合条件的反馈' }}
        </div>
        <div class="empty-desc">
          {{ filteredFeedbackList.length > 0 ? '已经显示全部反馈' : '请尝试调整筛选条件' }}
        </div>
      </div>

      <!-- 新增：分页控件 -->
      <div class="pagination" v-if="filteredFeedbackList.length > 0">
        <button
          class="page-btn"
          @click="currentPage = 1"
          :disabled="currentPage === 1"
        >
          首页
        </button>
        <button
          class="page-btn"
          @click="currentPage--"
          :disabled="currentPage === 1"
        >
          上一页
        </button>
        <span class="page-info">
          第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
        </span>
        <button
          class="page-btn"
          @click="currentPage++"
          :disabled="currentPage === totalPages"
        >
          下一页
        </button>
        <button
          class="page-btn"
          @click="currentPage = totalPages"
          :disabled="currentPage === totalPages"
        >
          末页
        </button>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, watch } from 'vue'

// 定义Props接口
interface Props {
  pendingCount: number
  urgentCount: number
  feedbackList: FeedbackItem[]  // 接收父组件传递的列表
}
// 定义Emit接口
interface Emits {
  (e: 'feedbackProcessed', itemId: number): void
  (e: 'feedbackIgnored', itemId: number): void
}

// 反馈项接口
interface FeedbackItem {
  id: number
  time: string
  user: string
  content: {
    title: string
    desc: string
  }
  type: string
  status: '待处理' | '已处理'
  urgent?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const hoveredItem = ref<number | null>(null)

// 新增：筛选相关状态
const selectedType = ref('')
const selectedStatus = ref('')

// 新增：分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)

// 新增：获取所有唯一的反馈类型
const uniqueTypes = computed(() => {
  const types = new Set<string>()
  props.feedbackList.forEach(item => types.add(item.type))
  return Array.from(types)
})

// 新增：筛选后的列表
const filteredFeedbackList = computed(() => {
  return props.feedbackList.filter(item => {
    // 类型筛选
    if (selectedType.value && item.type !== selectedType.value) {
      return false
    }
    // 状态筛选
    if (selectedStatus.value && item.status !== selectedStatus.value) {
      return false
    }
    return true
  })
})

// 新增：总页数计算
const totalPages = computed(() => {
  return Math.ceil(filteredFeedbackList.value.length / pageSize.value)
})

// 新增：当前页数据
const currentPageData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  return filteredFeedbackList.value.slice(startIndex, endIndex)
})



// 新增：处理每页显示条数变化
const handlePageSizeChange = () => {
  currentPage.value = 1
}

// 新增：监听原始数据变化，重置筛选和分页
watch(
  () => props.feedbackList,
  () => {
    selectedType.value = ''
    selectedStatus.value = ''
    currentPage.value = 1
  }
)

// 格式化时间显示
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))

  if (diffMins < 60) {
    return `${diffMins}分钟前`
  } else if (diffHours < 24) {
    return `${diffHours}小时前`
  } else {
    return date.toLocaleDateString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).replace(/\//g, '-')
  }
}

// 处理反馈
const handleProcess = async (item: FeedbackItem) => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    const success = true
    if (success) {
      // 通知父组件反馈已处理
      emit('feedbackProcessed', item.id)
      console.log('处理反馈成功，通知父组件更新计数')
    }

  } catch (error) {
    console.error('处理反馈失败:', error)
  }
}

// 忽略反馈
const handleIgnore = async (item: FeedbackItem) => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))

    const success = true
    if (success) {
      // 通知父组件反馈已忽略
      emit('feedbackIgnored', item.id)
      console.log('忽略反馈成功，通知父组件更新计数')
    }

  } catch (error) {
    console.error('忽略反馈失败:', error)
  }
}
</script>

<style scoped>
/* 原有样式保持不变 */
.pending-feedback-card {
  width: 100%;
  margin: 10px 0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f2f5;
  overflow: hidden;
  transition: all 0.3s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.pending-feedback-card:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #f0f2f5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #409eff;
  width: 18px;
  height: 18px;
}

.title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 9px;
  background-color: #ff4d4f;
  color: #fff;
  font-size: 12px;
  font-weight: 500;
}

.urgent-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #ff4d4f;
  color: #fff;
  font-size: 12px;
}

.tag-icon {
  width: 12px;
  height: 12px;
}

.feedback-list {
  padding: 15px 20px;
}

.feedback-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feedback-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  border-radius: 8px;
  transition: all 0.2s ease;
  position: relative;
}

.feedback-item:hover {
  background-color: #f5f7fa;
}

.processed-item {
  opacity: 0.8;
  background-color: #f9fafb;
}

.processed-item:hover {
  background-color: #f9fafb;
}

.item-time {
  font-size: 12px;
  color: #9ca3af;
  min-width: 100px;
}

.item-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e8f4ff;
  color: #409eff;
  flex-shrink: 0;
}

.item-avatar svg {
  width: 18px;
  height: 18px;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.content-title {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.content-desc {
  color: #6b7280;
  font-size: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-type {
  flex-shrink: 0;
}

.type-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #d1e9ff;
  background-color: #ecf5ff;
  color: #409eff;
  font-size: 12px;
}

.item-status {
  flex-shrink: 0;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.processed-tag {
  background-color: #f0f9ff;
  color: #13c2c2;
  border: 1px solid #b5f5ec;
}

.item-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
  flex-shrink: 0;
}

.item-actions.show {
  opacity: 1;
}

.action-btn {
  padding: 4px 8px;
  border: none;
  background: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.process-btn {
  color: #409eff;
}

.process-btn:hover {
  background-color: rgba(64, 158, 255, 0.1);
}

.delete-btn {
  color: #ff4d4f;
}

.delete-btn:hover {
  background-color: rgba(255, 77, 79, 0.1);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #9ca3af;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  color: #d1d5db;
}

.empty-text {
  font-size: 16px;
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 14px;
  color: #d1d5db;
}

/* 新增：筛选和分页样式 */
.filters {
  display: flex;
  gap: 16px;
  padding: 12px 20px;
  border-bottom: 1px solid #f0f2f5;
  background-color: #fff;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #6b7280;
}

.filter-group select {
  padding: 4px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  color: #1f2937;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 0;
  border-top: 1px solid #f0f2f5;
  margin-top: 10px;
}

.page-btn {
  padding: 4px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background-color: #fff;
  color: #1f2937;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #f9fafb;
}

.page-btn:hover:not(:disabled) {
  background-color: #f5f7fa;
  border-color: #9ca3af;
}

.page-info {
  font-size: 14px;
  color: #6b7280;
}

.page-size {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 16px;
}

.page-size label {
  font-size: 14px;
  color: #6b7280;
}

.page-size select {
  padding: 4px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}
</style>
