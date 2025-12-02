<template>
  <div class="w-full h-full min-h-full relative bg-parchment overflow-hidden">
    <!-- 顶部标题 -->
    <div
      class="bg-gradient-to-r from-amber-600 to-amber-800 text-white p-6 shadow-lg z-10 relative"
    >
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-serif font-bold">校园打卡地图</h1>
          <p class="text-amber-100 mt-1">探索校园美景，记录美好时光</p>
        </div>
        <button
          @click="toggleListPanel"
          class="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all duration-300 flex items-center gap-2 backdrop-blur-sm border border-white/30"
        >
          <i :class="listPanelOpen ? 'fa-solid fa-times' : 'fa-solid fa-list'" class="text-lg"></i>
          <span class="font-medium">{{ listPanelOpen ? '关闭列表' : '查看列表' }}</span>
        </button>
      </div>
    </div>

    <!-- 侧边列表面板 -->
    <div
      :class="[
        'absolute left-0 top-[120px] w-80 bg-white/95 backdrop-blur-md shadow-2xl z-30 overflow-hidden border-r border-amber-200 h-[calc(100%-120px)]',
        isMounted ? 'transition-all duration-300 ease-in-out' : '',
        listPanelOpen ? 'translate-x-0' : '-translate-x-full',
      ]"
    >
      <div class="h-full flex flex-col">
        <!-- 列表标题 -->
        <div class="p-5 border-b border-amber-200 bg-gradient-to-r from-amber-50 to-amber-100">
          <h2 class="text-xl font-serif font-bold text-amber-900 flex items-center">
            <i class="fa-solid fa-map-pin mr-2 text-amber-600"></i>
            打卡点列表
            <span class="ml-2 text-sm bg-amber-600 text-white px-2 py-0.5 rounded-full">
              {{ filteredLocations.length }}
            </span>
          </h2>
        </div>

        <!-- 搜索框 -->
        <div class="p-4 border-b border-amber-200 bg-white">
          <div class="relative">
            <i
              class="fa-solid fa-search absolute left-3 top-1/2 -translate-y-1/2 text-amber-600"
            ></i>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索地点名称或描述..."
              class="w-full pl-10 pr-4 py-2 border border-amber-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent text-sm"
            />
          </div>
        </div>

        <!-- 列表内容 -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <div
            v-for="location in filteredLocations"
            :key="location.id"
            @click="focusLocation(location)"
            :class="[
              'p-4 rounded-lg border-2 cursor-pointer transition-all duration-300 hover:shadow-lg',
              activeLocationId === location.id
                ? 'border-amber-500 bg-amber-50 shadow-md'
                : 'border-amber-200 bg-white hover:border-amber-300',
            ]"
          >
            <div class="flex items-start gap-3">
              <img
                :src="location.thumbnail"
                :alt="location.name"
                class="w-16 h-16 rounded-lg object-cover flex-shrink-0"
              />
              <div class="flex-1 min-w-0">
                <h3 class="font-serif font-bold text-amber-900 mb-1 text-lg">
                  {{ location.name }}
                </h3>
                <p class="text-sm text-gray-600 line-clamp-2 mb-2">{{ location.description }}</p>
                <div class="flex items-center text-xs text-gray-500">
                  <i class="fa-solid fa-location-dot mr-1 text-amber-600"></i>
                  {{ getCoordinateString(location.coordinates) }}
                </div>
              </div>
            </div>
          </div>

          <div v-if="filteredLocations.length === 0" class="text-center py-8 text-gray-400">
            <i class="fa-solid fa-search text-2xl mb-2"></i>
            <p>未找到匹配的打卡点</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 地图容器 -->
    <div id="checkin-map" class="w-full h-[calc(100%-120px)] relative">
      <!-- 加载提示 -->
      <div
        v-if="mapLoading"
        class="absolute inset-0 bg-white/80 backdrop-blur-sm z-20 flex flex-col items-center justify-center"
      >
        <i class="fa-solid fa-circle-notch fa-spin text-4xl text-amber-700 mb-4"></i>
        <p class="text-gray-600 text-lg">地图加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import locationsData from './locations-data.json'

// 声明全局类型
declare global {
  interface Window {
    AMap: any
    AMapLoader: any
  }
}

const router = useRouter()
const locations = locationsData
const mapLoading = ref(true)
const listPanelOpen = ref(false)
const searchKeyword = ref('')
const activeLocationId = ref<number | null>(null)

let map: any = null
let markers: any[] = []
let infoWindow: any = null

const isMounted = ref(false)

// 获取格式化的坐标字符串
const getCoordinateString = (coordinates: any): string => {
  if (!coordinates || !Array.isArray(coordinates) || coordinates.length < 2) {
    return '坐标未知'
  }
  return `${coordinates[0].toFixed(4)}, ${coordinates[1].toFixed(4)}`
}

// 过滤后的位置列表
const filteredLocations = computed(() => {
  if (!searchKeyword.value.trim()) {
    return locations
  }
  const keyword = searchKeyword.value.toLowerCase()
  return locations.filter(
    (location) =>
      location.name.toLowerCase().includes(keyword) ||
      location.description.toLowerCase().includes(keyword),
  )
})

// 切换列表面板
const toggleListPanel = () => {
  listPanelOpen.value = !listPanelOpen.value
}

// 聚焦到指定位置
const focusLocation = (location: any) => {
  activeLocationId.value = location.id

  // 找到对应的标记点
  const marker = markers.find((m) => m.getExtData().id === location.id)
  if (marker && map && window.AMap) {
    // 关闭之前的信息窗口
    if (infoWindow) {
      infoWindow.close()
    }

    // 创建新的信息窗口
    infoWindow = new window.AMap.InfoWindow({
      content: createInfoWindowContent(location),
      offset: new window.AMap.Pixel(0, -10),
      autoMove: true,
      animateEnable: true,
      closeWhenClickMap: true,
      isCustom: true,
    })

    infoWindow.open(map, marker.getPosition())

    // 平滑移动到目标点 (false 表示启用动画)
    map.setZoomAndCenter(16, marker.getPosition(), false)
  }
}

// 计算地图中心点
const calculateMapCenter = () => {
  // 过滤出有效的坐标数据
  const validLocations = locations.filter(item =>
    item && item.coordinates && Array.isArray(item.coordinates) && item.coordinates.length >= 2
  )

  if (validLocations.length === 0) {
    return [119.2965, 26.0745] // 默认坐标（福州）
  }

  // 使用有效的坐标计算平均值
  const sumLng = validLocations.reduce((sum, item) => sum + (item.coordinates?.[0] || 0), 0)
  const sumLat = validLocations.reduce((sum, item) => sum + (item.coordinates?.[1] || 0), 0)

  return [sumLng / validLocations.length, sumLat / validLocations.length]
}

// 创建信息窗口内容
const createInfoWindowContent = (location: any) => {
  const infoWindowDiv = document.createElement('div')
  infoWindowDiv.className = 'info-window-content'
  infoWindowDiv.style.padding = '16px'
  infoWindowDiv.style.backgroundColor = '#fff'
  infoWindowDiv.style.borderRadius = '8px'
  infoWindowDiv.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)'
  infoWindowDiv.style.minWidth = '280px'

  infoWindowDiv.innerHTML = `
    <h3 style="margin: 0 0 8px 0; color: #78350f; font-size: 18px; font-weight: 600;">
      ${location.name}
    </h3>
    <p style="margin-bottom: 8px; line-height: 1.6; color: #5c4033; font-size: 14px;">
      ${location.description}
    </p>
    <div style="margin-top: 12px; display: flex; gap: 8px;">
      <button
        data-id="${location.id}"
        style="flex: 1; padding: 8px 16px; background: linear-gradient(135deg, #d97706, #f59e0b); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; transition: all 0.3s;"
      >
        查看详情
      </button>
    </div>
  `

  // 使用事件委托处理点击事件
  infoWindowDiv.querySelector('button[data-id]')?.addEventListener('click', (e) => {
    e.stopPropagation()
    const button = e.target as HTMLButtonElement
    const id = parseInt(button.getAttribute('data-id') || '0')
    router.push(`/checkin/${id}`)
  })

  return infoWindowDiv
}

// 初始化地图
const initMap = () => {
  if (!window.AMapLoader) {
    console.error('高德地图加载器未找到')
    mapLoading.value = false
    return
  }

  window.AMapLoader.load({
    key: 'd17c17f8f712c81a7e4241aff4faa7b0', // 使用示例中的 key，实际使用时请替换为您的 key
    version: '2.0',
    plugins: ['AMap.Marker', 'AMap.InfoWindow', 'AMap.ToolBar', 'AMap.Scale'],
  })
    .then((AMap: any) => {
      const center = calculateMapCenter()

      // 创建地图实例
      map = new AMap.Map('checkin-map', {
        zoom: 15,
        center: center,
        viewMode: '2D',
        resizeEnable: true,
        zoomEnable: true,
        dragEnable: true,
        animateEnable: true,
      })

      // 添加地图控件
      map.addControl(
        new AMap.ToolBar({
          position: 'RB',
          offset: new AMap.Pixel(15, 15),
          showZoomNum: true,
          showPosition: true,
        }),
      )
      map.addControl(
        new AMap.Scale({
          position: 'RB',
          offset: new AMap.Pixel(15, 80),
        }),
      )

      // 创建标记点
      markers = []
      locations.forEach((location, index) => {
        // 添加coordinates存在性检查
        if (!location.coordinates || !Array.isArray(location.coordinates) || location.coordinates.length < 2) {
          console.warn('无效的坐标数据:', location)
          return
        }
        // 创建正常状态的标记点
        const normalMarker = document.createElement('div')
        normalMarker.style.width = '20px'
        normalMarker.style.height = '20px'
        normalMarker.style.borderRadius = '50%'
        normalMarker.style.backgroundColor = '#d97706'
        normalMarker.style.border = '3px solid white'
        normalMarker.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)'
        normalMarker.style.transition = 'all 0.3s ease'
        normalMarker.style.cursor = 'pointer'

        // 创建悬停状态的标记点
        const hoverMarker = document.createElement('div')
        hoverMarker.style.width = '26px'
        hoverMarker.style.height = '26px'
        hoverMarker.style.borderRadius = '50%'
        hoverMarker.style.backgroundColor = '#f59e0b'
        hoverMarker.style.border = '3px solid white'
        hoverMarker.style.boxShadow = '0 4px 12px rgba(0,0,0,0.4)'
        hoverMarker.style.transition = 'all 0.3s ease'
        hoverMarker.style.cursor = 'pointer'

        const normalOffset = new AMap.Pixel(-10, -10)
        const hoverOffset = new AMap.Pixel(-13, -13)

        const marker = new AMap.Marker({
          position: [location.coordinates[0], location.coordinates[1]],
          content: normalMarker,
          offset: normalOffset,
          extData: location,
          anchor: 'center',
        })

        // 悬停效果
        marker.on('mouseover', () => {
          marker.setContent(hoverMarker)
          marker.setOffset(hoverOffset)
        })

        marker.on('mouseout', () => {
          marker.setContent(normalMarker)
          marker.setOffset(normalOffset)
        })

        // 点击显示信息窗口
        marker.on('click', (e: any) => {
          const data = e.target.getExtData()
          activeLocationId.value = data.id

          // 关闭之前的信息窗口
          if (infoWindow) {
            infoWindow.close()
          }

          // 创建新的信息窗口
          infoWindow = new AMap.InfoWindow({
            content: createInfoWindowContent(data),
            offset: new AMap.Pixel(0, -10),
            autoMove: true,
            animateEnable: true,
            closeWhenClickMap: true,
            isCustom: true,
          })

          infoWindow.open(map, e.target.getPosition())

          // 平滑移动到目标点 (false 表示启用动画)
          map.setZoomAndCenter(16, e.target.getPosition(), false)
        })

        map.add(marker)
        markers.push(marker)

        // 添加标记点渐入动画
        setTimeout(
          () => {
            normalMarker.style.opacity = '1'
            normalMarker.style.transform = 'scale(1)'
          },
          100 + index * 50,
        )
      })

      mapLoading.value = false

      // 监听窗口大小变化，自动调整地图大小
      window.addEventListener('resize', handleMapResize)
    })
    .catch((e: any) => {
      console.error('地图加载失败:', e)
      mapLoading.value = false
    })
}

// 处理地图大小调整
const handleMapResize = () => {
  if (map) {
    setTimeout(() => {
      map.getSize()
    }, 100)
  }
}

// 全局函数，供信息窗口中的按钮调用
if (typeof window !== 'undefined') {
  ;(window as any).openLocationDetail = (id: number) => {
    router.push(`/checkin/${id}`)
  }
}

onMounted(() => {
  setTimeout(() => {
    isMounted.value = true
  }, 100)

  // 等待 DOM 加载完成后再初始化地图
  setTimeout(() => {
    initMap()
  }, 100)
})

onUnmounted(() => {
  // 清理地图实例
  if (map) {
    map.destroy()
    map = null
  }
  markers = []
  if (infoWindow) {
    infoWindow.close()
    infoWindow = null
  }
})
</script>

<style scoped>
#checkin-map {
  min-height: 500px;
}

/* 地图控件样式优化 */
:deep(.amap-toolbar) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  overflow: hidden;
}

:deep(.amap-scale) {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  padding: 4px 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 列表滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f9f4ef;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: #d97706;
  border-radius: 3px;
  transition: background-color 0.3s;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: #b45309;
}

/* 列表项动画 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 信息窗口弹性动画 */
:deep(.info-window-content) {
  animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: center bottom;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3) translateY(20px);
  }
  50% {
    opacity: 1;
    transform: scale(1.05) translateY(-5px);
  }
  70% {
    transform: scale(0.95) translateY(0);
  }
  100% {
    transform: scale(1) translateY(0);
  }
}
</style>
