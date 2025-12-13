<template>
  <!-- 弹幕在整个网页上显示 -->
  <div class="fixed inset-0 pointer-events-none z-50 overflow-hidden">
    <div
      v-for="(item, index) in displayDanmaku"
      :key="item.id"
      class="absolute whitespace-nowrap text-amber-900 font-medium px-4 py-2 bg-white/80 rounded-full shadow-md border border-amber-200 pointer-events-none"
      :style="getDanmakuStyle(item)"
    >
      <i class="fa-solid fa-quote-left text-xs mr-1 opacity-50"></i>
      {{ item.content }}
      <i class="fa-solid fa-quote-right text-xs ml-1 opacity-50"></i>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

const props = defineProps<{
  locationId: number
}>()

interface DanmakuItem {
  id: number
  content: string
  left: number
  top: number
  speed: number
}

const danmakuList = ref<DanmakuItem[]>([])
const displayDanmaku = ref<DanmakuItem[]>([])
let animationFrameId: number | null = null

const fetchDanmaku = async () => {
  try {
    const token = localStorage.getItem('token')
    const url = getApiUrl(API_ENDPOINTS.CHECKIN_DANMAKU(props.locationId))
    console.log('Fetching danmaku from:', url)

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    console.log('Danmaku response status:', response.status, response.ok)

    if (response.ok) {
      const data = await response.json()
      console.log('Received danmaku data:', data)
      console.log('Number of danmaku items:', data.length)
      // 只获取纯文字打卡（作为弹幕）
      danmakuList.value = data.map((item: any, index: number) => ({
        id: item.id,
        content: item.content,
        left: window.innerWidth + index * 200,
        top: Math.random() * (window.innerHeight - 200) + 100, // 随机高度，避开顶部和底部
        speed: Math.random() * 0.5 + 0.5, // 随机速度 0.5-1px/frame
      }))

      displayDanmaku.value = danmakuList.value.slice(0, 5) // 最多显示5条
      console.log('Displaying danmaku:', displayDanmaku.value.length, 'items')
    } else {
      const errorText = await response.text()
      console.error('Failed to fetch danmaku:', response.status, errorText)
    }
  } catch (error) {
    console.error('Failed to fetch danmaku:', error)
  }
}

const getDanmakuStyle = (item: DanmakuItem) => {
  return {
    left: `${item.left}px`,
    top: `${item.top}px`,
    transition: 'none',
  }
}

const animate = () => {
  displayDanmaku.value.forEach((item) => {
    item.left -= item.speed

    // 如果弹幕完全离开屏幕，重新从右侧进入
    if (item.left < -300) {
      item.left = window.innerWidth
      item.top = Math.random() * (window.innerHeight - 200) + 100
    }
  })

  animationFrameId = requestAnimationFrame(animate)
}

onMounted(() => {
  fetchDanmaku()
  animate()

  // 定期刷新弹幕内容
  const intervalId = setInterval(fetchDanmaku, 30000) // 每30秒刷新

  onUnmounted(() => {
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId)
    }
    clearInterval(intervalId)
  })
})

defineExpose({
  fetchDanmaku,
})
</script>
