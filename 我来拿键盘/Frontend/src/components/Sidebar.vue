<template>
  <div :class="panelClass" @mouseenter="hover = true" @mouseleave="hover = false">
    <button
      class="absolute top-4 right-2 p-1 rounded-full hover:bg-gray-200 transition-colors z-10"
      @click="toggleNav"
    >
      <div class="w-5 h-5 flex items-center justify-center">
        <div :class="iconClass" aria-hidden="true"></div>
      </div>
    </button>
    <div class="h-full w-full overflow-y-auto overflow-x-hidden py-16 px-0 relative" v-if="ui.navExpanded">
      <!-- 内容容器 -->
      <div class="flex flex-col items-center space-y-0 relative min-h-full">

        <!-- SVG背景层 - 放在底层 -->
        <!-- SVG背景层 - 放在底层 -->
        <div class="absolute top-0 left-0 w-full h-full z-0 pointer-events-none">
          <svg class="w-full h-full" style="overflow: visible;">
            <path v-for="(line, index) in lineCoords" :key="'line-'+index"
                  :d="`M ${line.x1} ${line.y1} L ${line.x2} ${line.y2}`"
                  fill="none"
                  stroke-width="2"
                  stroke-dasharray="6 4"
                  class="transition-colors duration-500"
                  :class="index < currentIndex ? 'stroke-green-500' : 'stroke-gray-300'"
            />
          </svg>
        </div>

        <!-- 遍历节点 -->
        <div v-for="(node, index) in mapNodes" :key="index" class="flex flex-col items-center w-full relative z-10"
             :style="{ transform: index % 2 === 0 ? 'translateX(-48px)' : 'translateX(48px)' }">

          <!-- 节点容器 -->
          <div
            class="relative cursor-pointer group flex flex-col items-center justify-center mb-32 last:mb-0"
            @click="navigateTo(node.path)"
          >
            <!-- 节点圆圈 -->
            <div
              ref="nodeRefs"
              class="w-10 h-10 rounded-full border-2 flex items-center justify-center transition-all duration-500 bg-white shadow-md z-20"
              :class="getNodeClass(index)"
            >
              <i v-if="index === currentIndex" class="fa-solid fa-person-walking text-amber-600 text-base animate-bounce"></i>
              <i v-else-if="index < currentIndex" class="fa-solid fa-check text-green-500 text-sm"></i>
              <span v-else class="text-xs text-gray-400 font-serif">{{ index + 1 }}</span>
            </div>

            <!-- 节点标签 -->
            <div class="absolute top-12 whitespace-nowrap font-serif text-sm transition-colors duration-300 bg-white/80 px-2 py-0.5 rounded-full backdrop-blur-sm shadow-sm border border-gray-100"
                 :class="getTextClass(index)">
              {{ node.name }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 收起状态下的简略显示 -->
    <div v-else class="h-full w-full flex flex-col items-center py-20 space-y-8">
      <div v-for="(node, index) in mapNodes" :key="index" class="w-2 h-2 rounded-full transition-colors duration-300"
           :class="index <= currentIndex ? 'bg-green-500' : 'bg-gray-300'">
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Window {
  FontAwesome?: any
}

import { computed, ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useRoute, useRouter } from 'vue-router'

const ui = useUiStore()
const hover = ref(false)
const isMounted = ref(false)
const isFirstLoad = ref(true)
const isRouteChanging = ref(false)
const route = useRoute()
const router = useRouter()

// 节点引用
const nodeRefs = ref<HTMLElement[]>([])
// 线条坐标
const lineCoords = ref<{x1: number, y1: number, x2: number, y2: number}[]>([])

// 地图节点定义
const mapNodes = [
  { name: '首页', path: '/home' },
  { name: '校史馆', path: '/history' },
  { name: '校园打卡', path: '/checkin' },
  { name: '学院介绍', path: '/college' },
  { name: '趣味游戏', path: '/game' },
  { name: '结束', path: '/end' },
]

// 更新线条坐标
const updateLines = () => {
  if (!ui.navExpanded || nodeRefs.value.length === 0) return

  const coords: {x1: number, y1: number, x2: number, y2: number}[] = []

  // 获取容器的边界
  const container = nodeRefs.value[0]?.closest('.relative.min-h-full') as HTMLElement
  if (!container) return
  const containerRect = container.getBoundingClientRect()

  for (let i = 0; i < mapNodes.length - 1; i++) {
    const currentNode = nodeRefs.value[i]
    const nextNode = nodeRefs.value[i + 1]

    if (currentNode && nextNode) {
      const rect1 = currentNode.getBoundingClientRect()
      const rect2 = nextNode.getBoundingClientRect()

      // 获取节点的父容器（包含 transform 的容器）
      const nodeContainer1 = currentNode.closest('.flex.flex-col.items-center') as HTMLElement
      const nodeContainer2 = nextNode.closest('.flex.flex-col.items-center') as HTMLElement

      // 计算节点圆心的实际位置（考虑 transform 偏移）
      // 节点在容器中心，但容器可能有 translateX 偏移
      const containerCenterX = containerRect.left + containerRect.width / 2

      // 第一个节点的 x 坐标（考虑 translateX）
      const offset1 = i % 2 === 0 ? -48 : 48
      const x1 = containerCenterX + offset1
      const y1 = rect1.top + rect1.height / 2 - containerRect.top

      // 第二个节点的 x 坐标（考虑 translateX）
      const offset2 = (i + 1) % 2 === 0 ? -48 : 48
      const x2 = containerCenterX + offset2
      const y2 = rect2.top + rect2.height / 2 - containerRect.top

      coords.push({ x1, y1, x2, y2 })
    }
  }
  lineCoords.value = coords
}

// 监听窗口大小变化
let resizeObserver: ResizeObserver | null = null

// 计算当前所在的节点索引
const currentIndex = computed(() => {
  const currentPath = route.path
  console.log('Sidebar - 当前路由路径:', currentPath)

  // 首先尝试精确匹配
  let idx = mapNodes.findIndex(node => node.path === currentPath)

  // 如果找不到精确匹配，尝试查找父路径匹配
  if (idx === -1) {
    idx = mapNodes.findIndex(node => {
      // 只对有子路径的情况进行父路径匹配（不以/结尾的路径）
      if (node.path === '/' || node.path.endsWith('/')) return false
      return currentPath.startsWith(`${node.path}/`)
    })
  }

  console.log('Sidebar - 匹配到的节点索引:', idx)
  return idx === -1 ? 0 : idx
})

// 导航跳转
const navigateTo = (path: string) => {
  router.push(path)
}

// 获取节点样式
const getNodeClass = (index: number) => {
  if (index === currentIndex.value) {
    return 'border-amber-500 scale-110 ring-2 ring-amber-100'
  } else if (index < currentIndex.value) {
    return 'border-green-500 bg-green-50'
  } else {
    return 'border-gray-300 hover:border-amber-300'
  }
}

// 获取文字样式
const getTextClass = (index: number) => {
  if (index === currentIndex.value) {
    return 'text-amber-700 font-bold'
  } else if (index < currentIndex.value) {
    return 'text-green-600'
  } else {
    return 'text-gray-400 group-hover:text-amber-600'
  }
}

// 图标类
const iconClass = computed(() => {
  const baseClass = 'fa-solid w-full h-full flex items-center justify-center'
  const iconName = ui.navExpanded ? 'fa-chevron-left' : 'fa-chevron-right'
  return `${baseClass} ${iconName}`
})

// 面板类
const panelClass = computed(() => {
  const baseClasses =
    'fixed left-0 top-0 h-full bg-white/90 backdrop-blur-md border-r border-black/10 z-[90] rounded-tr-xl rounded-br-xl transition-all duration-300 ease-in-out'

  let classes = baseClasses

  if (ui.navExpanded) {
    classes += ' w-48 shadow-2xl'
  } else {
    classes += ' w-12 bg-white/60 shadow'
  }

  return classes
})

const toggleNav = () => {
  ui.navExpanded = !ui.navExpanded
  isFirstLoad.value = false
  // 展开动画完成后更新线条
  setTimeout(updateLines, 350)
}

// 监听路由变化
watch(
  () => route.path,
  () => {
    isMounted.value = false
    setTimeout(() => {
      isMounted.value = true
      isRouteChanging.value = true
      setTimeout(() => {
        isRouteChanging.value = false
      }, 1000)
    }, 10)
  },
)

// 监听展开状态变化，重新计算线条
watch(() => ui.navExpanded, (expanded) => {
  if (expanded) {
    // 等待DOM更新和动画完成
    nextTick(() => {
      setTimeout(updateLines, 350)
    })
  }
})

onMounted(() => {
  setTimeout(() => {
    isMounted.value = true
  }, 10)

  setTimeout(() => {
    isFirstLoad.value = false
  }, 80)

  // 初始化线条
  nextTick(() => {
    setTimeout(updateLines, 500)
  })

  // 设置ResizeObserver
  const container = document.querySelector('.h-full.w-full.overflow-y-auto')
  if (container) {
    resizeObserver = new ResizeObserver(() => {
      updateLines()
    })
    resizeObserver.observe(container)
  }

  window.addEventListener('resize', updateLines)
})

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  window.removeEventListener('resize', updateLines)
})
</script>

<style scoped>
/* 移除之前的复杂动画，使用 Tailwind 的 transition */
.animate-bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-10%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(10%);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
</style>
