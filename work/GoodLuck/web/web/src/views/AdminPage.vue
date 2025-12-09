<template>
  <Info :data="dashboardData" />
  <!-- 登录量图表（从父组件传递数据） -->
  <LoginChart :chart-data="chartData" :loading="loading" />
  <PendingFeedbackCard
    :pending-count="dashboardData.pendingFeedback"
    :urgent-count="feedbackData.urgentCount"
    :feedback-list="feedbackData.list"
    @feedback-processed="handleFeedbackProcessed"
    @feedback-ignored="handleFeedbackIgnored"
  />
  <MediaManagement
    :videos="videoList"
    :loading="videoLoading"
    @video-upload="handleVideoUpload"
    @video-delete="handleVideoDelete"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'

import Info from '@/components/admin/Info.vue'
import LoginChart from '@/components/admin/LoginChart.vue'
import PendingFeedbackCard from '@/components/admin/PendingFeedback.vue'
import MediaManagement from '@/components/admin/MediaManage.vue'

// 定义数据类型接口
interface DashboardData {
  loginCount: number
  onlineUsers: number
  pendingFeedback: number
  mediaFiles: number
}

interface ApiResponse<T> {
  code: number
  data: T
  message: string
  success: boolean
}

interface FeedbackData {
  list: any[]
  urgentCount: number
  totalCount: number
}

interface ChartData {
  loginData: number[]
  activeData: number[]
  dates: string[]
  dateRange: string
  totalLogin: number
  totalActive: number
}

interface VideoItem {
  id: number
  name: string
  annotation: string
  uploadTime: string
  size: number
  url?: string
  duration?: number
}

interface UploadFormData {
  name: string
  annotation: string
  file: File
}

// API基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api'

// 响应式数据
const dashboardData = ref<DashboardData>({
  loginCount: 0,
  onlineUsers: 0,
  pendingFeedback: 0,
  mediaFiles: 0,
})

const feedbackData = ref<FeedbackData>({
  list: [],
  urgentCount: 0,
  totalCount: 0,
})

const chartData = ref<ChartData>({
  loginData: [],
  activeData: [],
  dates: [],
  dateRange: '',
  totalLogin: 0,
  totalActive: 0,
})

const videoList = ref<VideoItem[]>([])
const videoLoading = ref(false)
const loading = ref(true)
const error = ref<string | null>(null)

// ========== API请求工具函数 ==========
const apiRequest = async (url: string, options: RequestInit = {}) => {
  const token = localStorage.getItem('token') || ''// 从本地存储获取token

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: token ? `Bearer ${token}` : '',
      ...options.headers,
    },
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...defaultOptions,
      ...options,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (err) {
    console.error('API请求失败:', err)
    throw err
  }
}

// ========== API接口调用函数 ==========

/**
 * 获取仪表板统计数据
 */
const fetchDashboardStats = async () => {
  return await apiRequest('/admin/dashboard/stats')
}

/**
 * 获取登录图表数据
 */
const fetchChartData = async () => {
  return await apiRequest('/admin/dashboard/chart-data')
}

/**
 * 获取待处理反馈列表
 */
const fetchPendingFeedback = async () => {
  return await apiRequest('/admin/feedback/pending')
}

/**
 * 获取视频列表
 */
const fetchVideos = async () => {
  return await apiRequest('/admin/media/videos')
}

/**
 * 上传视频
 */
const uploadVideo = async (formData: FormData) => {
  return await apiRequest('/api/admin/media/upload', {
    method: 'POST',
    headers: {
      // 注意：上传文件时不要设置Content-Type，浏览器会自动设置正确的boundary
      Authorization: localStorage.getItem('token')
        ? `Bearer ${localStorage.getItem('token')}`
        : '',
    },
    body: formData,
  })
}

/**
 * 删除视频
 */
const deleteVideo = async (videoId: number) => {
  return await apiRequest(`/admin/media/videos/${videoId}`, {
    method: 'DELETE',
  })
}

/**
 * 处理反馈
 */
const processFeedback = async (feedbackId: number) => {
  return await apiRequest(`/admin/feedback/${feedbackId}/process`, {
    method: 'PUT',
  })
}

/**
 * 忽略反馈
 */
const ignoreFeedback = async (feedbackId: number) => {
  return await apiRequest(`/admin/feedback/${feedbackId}/ignore`, {
    method: 'PUT',
  })
}

// ========== 计算属性 ==========
const pendingCount = computed(() => {
  return feedbackData.value.list.filter((item) => item.status === '待处理').length
})

const urgentCount = computed(() => {
  return feedbackData.value.list.filter((item) => item.urgent && item.status === '待处理').length
})

// ========== 监听器 ==========
watch(
  videoList,
  (newVideos) => {
    dashboardData.value.mediaFiles = newVideos.length
    console.log('视频数量变化，同步更新媒体文件数:', newVideos.length)
  },
  { deep: true },
)

// ========== 事件处理函数 ==========

/**
 * 处理视频上传事件
 */
const handleVideoUpload = async (formData: UploadFormData) => {
  try {
    console.log('主组件收到视频上传请求:', formData.name)

    // 创建FormData对象用于文件上传
    const uploadFormData = new FormData()
    uploadFormData.append('name', formData.name)
    uploadFormData.append('annotation', formData.annotation)
    uploadFormData.append('file', formData.file)

    // 调用上传API
    const newVideo = await uploadVideo(uploadFormData)

    // 添加到本地列表
    videoList.value.unshift(newVideo)

    console.log('上传后视频数量:', videoList.value.length)
    return newVideo
  } catch (error) {
    console.error('视频上传失败:', error)
    throw error
  }
}

/**
 * 处理视频删除事件
 */
const handleVideoDelete = async (videoId: number) => {
  try {
    console.log('主组件收到视频删除请求，视频ID:', videoId)

    // 调用删除API
    const success = await deleteVideo(videoId)

    if (success) {
      // 从本地列表移除
      videoList.value = videoList.value.filter((video) => video.id !== videoId)
      console.log('删除后视频数量:', videoList.value.length)
    }

    return success
  } catch (error) {
    console.error('视频删除失败:', error)
    throw error
  }
}

/**
 * 处理反馈处理事件
 */
const handleFeedbackProcessed = async (itemId: number) => {
  try {
    console.log('父组件收到反馈处理事件，项目ID:', itemId)

    // 调用API处理反馈
    await processFeedback(itemId)

    // 更新本地状态
    const itemIndex = feedbackData.value.list.findIndex((item) => item.id === itemId)
    if (itemIndex !== -1) {
      feedbackData.value.list[itemIndex].status = '已处理'
      dashboardData.value.pendingFeedback = pendingCount.value
      console.log('本地状态更新完成，当前待处理数量:', dashboardData.value.pendingFeedback)
    }
  } catch (error) {
    console.error('处理反馈更新失败:', error)
    throw error
  }
}

/**
 * 处理反馈忽略事件
 */
const handleFeedbackIgnored = async (itemId: number) => {
  try {
    console.log('父组件收到反馈忽略事件，项目ID:', itemId)

    // 调用API忽略反馈
    await ignoreFeedback(itemId)

    // 更新本地状态
    feedbackData.value.list = feedbackData.value.list.filter((item) => item.id !== itemId)
    dashboardData.value.pendingFeedback = pendingCount.value
    feedbackData.value.urgentCount = urgentCount.value
    feedbackData.value.totalCount = feedbackData.value.list.length

    console.log('反馈已忽略，当前待处理数量:', dashboardData.value.pendingFeedback)
  } catch (error) {
    console.error('忽略反馈更新失败:', error)
    throw error
  }
}

// ========== 数据初始化函数 ==========

/**
 * 初始化视频数据
 */
const initVideoData = async () => {
  try {
    console.log('初始化视频数据...')
    videoLoading.value = true
    const videos = await fetchVideos()
    videoList.value = videos
    console.log('视频数据初始化完成，视频数量:', videos.length)
  } catch (error) {
    console.error('初始化视频数据失败:', error)
    throw error
  } finally {
    videoLoading.value = false
  }
}

/**
 * 获取仪表板数据
 */
const fetchData = async () => {
  try {
    console.log('开始调用API...')
    loading.value = true

    // 并行请求所有数据
    const [statsData, chartDataResponse, feedbackDataResponse] = await Promise.all([
      fetchDashboardStats(),
      fetchChartData(),
      fetchPendingFeedback(),
    ])

    console.log('API返回数据:', { statsData, chartDataResponse, feedbackDataResponse })

    // 更新数据
    dashboardData.value = {
      ...statsData,
      mediaFiles: videoList.value.length, // 使用实际的视频数量
    }

    chartData.value = chartDataResponse
    feedbackData.value = feedbackDataResponse

    // 确保pendingFeedback与实际的待处理数量一致
    dashboardData.value.pendingFeedback = pendingCount.value
    feedbackData.value.urgentCount = urgentCount.value

    console.log('数据更新完成，待处理数量:', dashboardData.value.pendingFeedback)
  } catch (err) {
    console.error('数据获取失败:', err)
    error.value = '数据获取失败'
  } finally {
    loading.value = false
    console.log('Loading状态设置为false')
  }
}

// ========== 组件挂载 ==========
onMounted(async () => {
  console.log('管理员仪表板组件挂载，开始初始化数据...')

  try {
    // 先初始化视频数据
    await initVideoData()

    // 再获取其他仪表盘数据
    await fetchData()

    console.log('所有数据初始化完成，最终媒体文件数:', dashboardData.value.mediaFiles)
  } catch (err) {
    console.error('数据初始化失败:', err)
    error.value = '数据初始化失败，请检查网络连接或重新登录'
  }
})
</script>
