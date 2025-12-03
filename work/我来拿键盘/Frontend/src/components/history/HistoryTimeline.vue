<template>
  <div class="flex flex-col md:flex-row h-full overflow-hidden bg-parchment pt-14">
    <!-- 左侧固定区域：显示当前图片 -->
    <div class="w-full md:w-1/2 h-1/2 md:h-full relative overflow-hidden border-b md:border-b-0 md:border-r border-amber-900/20 flex items-center justify-center p-8 bg-amber-50/30">
      <!-- 图片外框容器 -->
      <div class="relative w-full max-w-2xl max-h-[calc(100vh-8rem)] aspect-[4/3] border-8 border-white shadow-2xl rotate-1 transform transition-all duration-700 hover:rotate-0">
        <!-- 装饰性边角 -->
        <div class="absolute -top-2 -left-2 w-8 h-8 border-t-4 border-l-4 border-amber-800/40 z-20"></div>
        <div class="absolute -top-2 -right-2 w-8 h-8 border-t-4 border-r-4 border-amber-800/40 z-20"></div>
        <div class="absolute -bottom-2 -left-2 w-8 h-8 border-b-4 border-l-4 border-amber-800/40 z-20"></div>
        <div class="absolute -bottom-2 -right-2 w-8 h-8 border-b-4 border-r-4 border-amber-800/40 z-20"></div>

        <transition-group name="fade-image">
          <div
            v-for="item in historyData"
            :key="item.id"
            v-show="currentId === item.id"
            class="absolute inset-0 w-full h-full bg-gray-100"
          >
            <img
              :src="item.image"
              :alt="item.title"
              class="w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex items-end p-6">
              <div class="text-white transform translate-y-0 transition-transform duration-500">
                <div class="text-5xl font-serif font-bold mb-1 opacity-90 text-amber-100">{{ item.year }}</div>
                <div class="text-xl font-serif tracking-wider">{{ item.title }}</div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>

    <!-- 右侧滚动区域：时间轴列表 -->
    <div class="w-full md:w-1/2 h-1/2 md:h-full overflow-y-auto relative scroll-smooth bg-parchment" ref="scrollContainer">
      <div class="flex flex-col py-[300%]">
        <div class="relative border-l-2 border-amber-800/30 ml-12 md:ml-24 space-y-32 pr-8 md:pr-16 max-w-xl">
          <div
            v-for="(item, index) in historyData"
            :key="item.id"
            :ref="el => setItemRef(el, item.id)"
            class="relative pl-8 md:pl-12 group transition-all duration-700 ease-out cursor-pointer"
            :class="currentId === item.id ? 'opacity-100 translate-x-0 scale-100' : 'opacity-40 translate-x-4 scale-95 blur-[1px]'"
            @click="scrollToItem(item.id)"
          >
            <!-- 时间轴节点 -->
            <div
              class="absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 transition-all duration-500 z-10"
              :class="currentId === item.id ? 'bg-amber-600 border-amber-200 scale-150 shadow-[0_0_15px_rgba(217,119,6,0.6)]' : 'bg-parchment border-amber-800/50'"
            ></div>

            <!-- 内容卡片 -->
            <div class="space-y-3">
              <div class="flex items-baseline space-x-4">
                <span class="text-3xl font-serif font-bold transition-colors duration-300"
                      :class="currentId === item.id ? 'text-amber-800' : 'text-gray-400'">
                  {{ item.year }}
                </span>
                <h3 class="text-xl font-bold transition-colors duration-300"
                    :class="currentId === item.id ? 'text-gray-900' : 'text-gray-500'">
                  {{ item.title }}
                </h3>
              </div>

              <p class="leading-relaxed text-justify font-serif transition-colors duration-300"
                 :class="currentId === item.id ? 'text-gray-700' : 'text-gray-400'">
                {{ item.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import historyDataRaw from './history-data.json'

interface HistoryItem {
  id: number
  year: string
  title: string
  description: string
  image: string
}

const historyData = ref<HistoryItem[]>(historyDataRaw)
const currentId = ref(historyData.value[0]?.id || 1)
const scrollContainer = ref<HTMLElement | null>(null)
const itemRefs = ref<Map<number, Element>>(new Map())

// 收集节点引用
const setItemRef = (el: any, id: number) => {
  if (el) {
    itemRefs.value.set(id, el)
  }
}

// 滚动到指定项目
const scrollToItem = (id: number) => {
  const element = itemRefs.value.get(id)
  if (element && scrollContainer.value) {
    // 计算元素相对于容器的位置，使其滚动到容器的上半部分
    const elementRect = element.getBoundingClientRect()
    const containerRect = scrollContainer.value.getBoundingClientRect()
    const offset = elementRect.top - containerRect.top - containerRect.height / 3

    scrollContainer.value.scrollBy({
      top: offset,
      behavior: 'smooth'
    })

    // 直接更新当前ID以提供即时反馈
    currentId.value = id
  }
}

// Intersection Observer 实例
let observer: IntersectionObserver | null = null

onMounted(() => {
  // 设置 Intersection Observer
  const options = {
    root: scrollContainer.value,
    rootMargin: '-15% 0px -75% 0px', // 调整触发区域，使其更容易触发
    threshold: 0.1 // 当元素有10%可见时触发
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // 找到对应的 ID
        for (const [id, el] of itemRefs.value.entries()) {
          if (el === entry.target) {
            currentId.value = id
            break
          }
        }
      }
    })
  }, options)

  // 观察所有节点
  itemRefs.value.forEach((el) => {
    observer?.observe(el)
  })
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.bg-parchment {
  background-color: #fdfbf7;
}

/* 图片淡入淡出动画 */
.fade-image-enter-active,
.fade-image-leave-active {
  transition: opacity 1s ease;
}

.fade-image-enter-from,
.fade-image-leave-to {
  opacity: 0;
}

/* 隐藏滚动条但保留功能 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}
.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}
.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(146, 64, 14, 0.2);
  border-radius: 3px;
}
</style>
