<template>
  <div class="h-full w-full overflow-y-auto bg-parchment pt-14">
    <div v-if="location" class="max-w-6xl mx-auto px-6 py-8">
      <!-- 标题区 -->
      <div class="mb-6">
        <button
          @click="router.back()"
          class="mb-4 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          <i class="fa-solid fa-arrow-left mr-2"></i>返回
        </button>
        <h1 class="text-4xl font-serif font-bold text-amber-900 mb-2">{{ location.name }}</h1>
        <p class="text-gray-600">{{ location.description }}</p>
      </div>

      <!-- 图片轮播 -->
      <div class="mb-8 relative bg-white rounded-2xl shadow-lg p-4 border-4 border-amber-800/20">
        <div class="flex overflow-x-auto gap-4 pb-4 scroll-smooth snap-x" ref="galleryRef">
          <div
            v-for="(image, index) in location.images"
            :key="index"
            class="flex-shrink-0 w-full md:w-[600px] h-[400px] rounded-xl overflow-hidden snap-start border-4 border-white shadow-md"
          >
            <img
              :src="image"
              :alt="`${location.name} - ${index + 1}`"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

        <!-- 滚动提示 -->
        <div class="text-center text-sm text-gray-500 mt-2">
          <i class="fa-solid fa-hand-pointer mr-1"></i> 左右滑动查看更多图片
        </div>
      </div>

      <!-- 详细介绍 -->
      <div
        class="mb-8 bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-md border-2 border-amber-200"
      >
        <h2 class="text-2xl font-serif font-bold text-amber-800 mb-4">详细介绍</h2>
        <p class="text-gray-700 leading-relaxed font-serif">{{ location.detailedDescription }}</p>
        <div class="mt-4 text-sm text-gray-500">
          <i class="fa-solid fa-location-dot mr-2"></i>
          坐标: {{ location.coordinates.join(', ') }}
        </div>
      </div>

      <!-- 弹幕区域 -->
      <DanmakuScroll ref="danmakuScrollRef" :locationId="location.id" class="mb-8" />

      <!-- 打卡表单 -->
      <CheckinForm :locationId="location.id" @submitted="handleCheckinSubmitted" class="mb-8" />

      <!-- 打卡区（评论区） -->
      <div class="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-md border-2 border-amber-200">
        <h2 class="text-2xl font-serif font-bold text-amber-800 mb-4">
          <i class="fa-solid fa-comments mr-2"></i>打卡墙
        </h2>

        <div v-if="checkins.length === 0" class="text-center text-gray-400 py-8">
          暂无打卡记录，快来第一个打卡吧！
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="checkin in displayedCheckins"
            :key="checkin.id"
            class="p-4 bg-parchment rounded-xl border-2 border-amber-300/50 shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="flex items-start gap-3">
              <!-- 头像 -->
              <div
                class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 border-2 border-amber-200"
              >
                <img
                  v-if="checkin.avatarUrl"
                  :src="getFullAvatarUrl(checkin.avatarUrl, 'avatar')"
                  :alt="`${checkin.userName}的头像`"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full bg-amber-200 flex items-center justify-center">
                  <i class="fa-solid fa-user text-amber-700"></i>
                </div>
              </div>

              <!-- 内容 -->
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-semibold text-gray-800">{{ checkin.userName }}</span>
                  <span class="text-xs text-gray-500">{{ formatTime(checkin.createdAt) }}</span>
                </div>
                <p class="text-gray-700 mb-2">{{ checkin.content }}</p>
                <div v-if="checkin.imageUrl" class="mt-2">
                  <img
                    :src="getFullAvatarUrl(checkin.imageUrl, 'image')"
                    alt="打卡图片"
                    class="max-w-xs rounded-lg border-2 border-amber-200"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载更多按钮 -->
        <div v-if="checkins.length > displayCount" class="text-center mt-6">
          <button
            @click="loadMore"
            class="px-6 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition-colors"
          >
            加载更多 <i class="fa-solid fa-chevron-down ml-2"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="flex items-center justify-center h-screen">
      <div class="text-center">
        <i class="fa-solid fa-circle-notch fa-spin text-4xl text-amber-700 mb-4"></i>
        <p class="text-gray-600">加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApiUrl, getStaticUrl, API_ENDPOINTS, STATIC_ENDPOINTS } from '@/config/api'
import locationsData from '@/components/checkin/locations-data.json'
import CheckinForm from '@/components/checkin/CheckinForm.vue'
import DanmakuScroll from '@/components/checkin/DanmakuScroll.vue'

// 处理头像URL和图片URL，确保是完整的后端URL
const getFullAvatarUrl = (url: string, type: string = 'avatar') => {
  console.log(`LocationDetail - 原始${type}URL:`, url)
  // 检查URL是否有效
  if (!url || url.trim() === '') {
    console.log(`LocationDetail - ${type}URL为空`)
    return getStaticUrl(STATIC_ENDPOINTS.AVATAR_DEFAULT)
  }
  // 检查是否是完整的HTTP/HTTPS链接
  if (url.startsWith('http://') || url.startsWith('https://')) {
    console.log(`LocationDetail - 使用完整${type}URL:`, url)
    return url
  }
  // 如果不是完整链接，添加后端基础URL
  const fullUrl = getApiUrl(url)
  console.log(`LocationDetail - 构建完整${type}URL:`, fullUrl)
  return fullUrl
}

interface Location {
  id: number
  name: string
  coordinates: [number, number]
  thumbnail: string
  description: string
  images: string[]
  detailedDescription: string
}

interface Checkin {
  id: number
  userName: string
  content: string
  imageUrl?: string
  createdAt: string
  avatarUrl?: string
}

const route = useRoute()
const router = useRouter()
const galleryRef = ref<HTMLElement | null>(null)
const danmakuScrollRef = ref<InstanceType<typeof DanmakuScroll> | null>(null)
const checkins = ref<Checkin[]>([])
const displayCount = ref(5)

const locationId = computed(() => parseInt(route.params.id as string))
const location = computed(
  () => locationsData.find((l) => l.id === locationId.value) as Location | undefined,
)
const displayedCheckins = computed(() => checkins.value.slice(0, displayCount.value))

const loadMore = () => {
  displayCount.value += 5
}

const formatTime = (time: string) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

const handleCheckinSubmitted = async () => {
  console.log('Check-in submitted! Refreshing...')
  // 刷新打卡列表
  await fetchCheckins()
  console.log('Check-in wall refreshed')
  // 刷新弹幕
  if (danmakuScrollRef.value) {
    danmakuScrollRef.value.fetchDanmaku()
    console.log('Danmaku refreshed')
  } else {
    console.error('danmakuScrollRef is null!')
  }
}

const fetchCheckins = async () => {
  try {
    const token = localStorage.getItem('token')
    console.log('Fetching checkins for location:', locationId.value)
    const url = getApiUrl(API_ENDPOINTS.CHECKIN_COMMENTS(locationId.value))
    console.log('Request URL:', url)

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    console.log('Response status:', response.status, response.ok)

    if (response.ok) {
      const data = await response.json()
      console.log('Received checkins data:', data)
      console.log('Number of checkins:', data.length)
      // 处理从后端获取的打卡数据，包含avatarUrl字段
      checkins.value = data
    } else {
      const errorText = await response.text()
      console.error('Failed to fetch checkins:', response.status, errorText)
    }
  } catch (error) {
    console.error('Failed to fetch checkins:', error)
  }
}

onMounted(() => {
  fetchCheckins()
})
</script>

<style scoped>
/* 滚动条样式 */
.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
}
.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #d4a574;
  border-radius: 4px;
}
.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #b8935f;
}
</style>
