<template>
  <div class="min-h-screen bg-parchment pt-14">
    <!-- 核心内容容器：v-if 和 v-else 保持相邻 -->
    <div v-if="college" class="max-w-[90rem] mx-auto p-8">
      <div class="flex-1 min-w-0">
        <!-- 返回按钮 -->
        <button
          @click="router.back()"
          class="mb-6 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          <i class="fa-solid fa-arrow-left mr-2"></i>返回
        </button>

        <!-- 学院封面与标题 -->
        <div class="mb-8 relative h-80 rounded-2xl overflow-hidden shadow-2xl">
          <img :src="college.cover" :alt="college.name" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
          <div class="absolute bottom-8 left-8 text-white">
            <h1 class="text-5xl font-serif font-bold mb-2">{{ college.name }}</h1>
            <p class="text-xl text-amber-200">{{ college.description }}</p>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="space-y-32">
          <!-- 学院简介 -->
          <section id="introduction" class="scroll-mt-32">
            <h2 class="text-3xl font-serif font-bold text-amber-900 mb-6 flex items-center">
              <i class="fa-solid fa-book-open mr-3 text-amber-600"></i>
              学院简介
            </h2>
            <div
              class="bg-white/80 backdrop-blur-sm rounded-xl p-8 shadow-md border-2 border-amber-200"
            >
              <p class="text-lg text-gray-700 leading-relaxed">{{ college.introduction }}</p>
            </div>
          </section>

          <!-- 教师风采 -->
          <section id="teachers" class="scroll-mt-32">
            <h2 class="text-3xl font-serif font-bold text-amber-900 mb-6 flex items-center">
              <i class="fa-solid fa-chalkboard-user mr-3 text-amber-600"></i>
              教师风采
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div
                v-for="teacher in college.teachers"
                :key="teacher.name"
                class="bg-white/80 backdrop-blur-sm rounded-xl p-6 shadow-md border-2 border-amber-200 hover:shadow-xl transition-shadow"
              >
                <div class="flex items-start gap-4 mb-4">
                  <img
                    :src="teacher.photo"
                    :alt="teacher.name"
                    class="w-20 h-20 rounded-full object-cover border-4 border-amber-100"
                  />
                  <div>
                    <h3 class="text-xl font-bold text-amber-900">{{ teacher.name }}</h3>
                    <p class="text-sm text-gray-600">{{ teacher.title }}</p>
                  </div>
                </div>
                <div class="space-y-2 text-sm">
                  <p class="text-gray-700">
                    <i class="fa-solid fa-flask mr-2 text-amber-600"></i>
                    研究方向：{{ teacher.research }}
                  </p>
                  <p class="text-gray-600">{{ teacher.achievements }}</p>
                </div>
              </div>
            </div>
          </section>

          <!-- 实验室介绍 -->
          <section id="labs" class="scroll-mt-32">
            <h2 class="text-3xl font-serif font-bold text-amber-900 mb-6 flex items-center">
              <i class="fa-solid fa-flask mr-3 text-amber-600"></i>
              实验室介绍
            </h2>
            <div class="space-y-6">
              <div
                v-for="lab in college.labs"
                :key="lab.name"
                class="bg-white/80 backdrop-blur-sm rounded-xl overflow-hidden shadow-md border-2 border-amber-200 hover:shadow-xl transition-shadow"
              >
                <div class="md:flex">
                  <div class="md:w-1/3">
                    <img :src="lab.image" :alt="lab.name" class="w-full h-64 object-cover" />
                  </div>
                  <div class="p-6 md:w-2/3">
                    <h3 class="text-2xl font-bold text-amber-900 mb-3">{{ lab.name }}</h3>
                    <p class="text-gray-700 mb-4">{{ lab.description }}</p>
                    <div class="bg-amber-50 rounded-lg p-4">
                      <p class="text-sm text-gray-600">
                        <i class="fa-solid fa-computer mr-2 text-amber-600"></i>
                        <strong>设备：</strong>{{ lab.equipment }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 学院论坛 -->
          <section id="forum" class="scroll-mt-32 pb-32">
            <h2 class="text-3xl font-serif font-bold text-amber-900 mb-6 flex items-center">
              <i class="fa-solid fa-comments mr-3 text-amber-600"></i>
              学院论坛
            </h2>

            <!-- 评论表单 -->
            <div class="mb-6">
              <CommentForm :college-id="college.id" @submitted="fetchComments" />
            </div>

            <!-- 评论列表 -->
            <div class="space-y-4">
              <div v-if="comments.length === 0" class="text-center py-12 bg-white/60 rounded-xl">
                <i class="fa-solid fa-message text-4xl text-gray-300 mb-3"></i>
                <p class="text-gray-500">还没有评论，快来发表第一条评论吧！</p>
              </div>

              <CommentItem
                v-for="comment in comments"
                :key="comment.id"
                :comment="comment"
                :current-user-id="currentUserId"
                @deleted="fetchComments"
                @liked="fetchComments"
              />
            </div>
          </section>
        </div>
      </div>
    </div>

    <!-- 加载状态：与 v-if 直接相邻 -->
    <div v-else class="flex items-center justify-center h-screen">
      <div class="text-center">
        <i class="fa-solid fa-circle-notch fa-spin text-4xl text-amber-700 mb-4"></i>
        <p class="text-gray-600">加载中...</p>
      </div>
    </div>

    <!-- 右侧悬浮导航按钮：移到 v-if/v-else 外部，避免打断相邻关系 -->
    <div class="fixed right-6 top-24 hidden md:flex flex-col gap-3 z-50">
      <button
        @click="scrollTo('introduction')"
        class="px-3 py-2 rounded-lg shadow border border-amber-100 transition-colors"
        :class="
          activeId === 'introduction'
            ? 'bg-amber-700 text-white'
            : 'bg-white/80 text-gray-700 hover:bg-gray-100'
        "
      >
        <i class="fa-solid fa-book-open mr-2"></i>简介
      </button>
      <button
        @click="scrollTo('teachers')"
        class="px-3 py-2 rounded-lg shadow border border-amber-100 transition-colors"
        :class="
          activeId === 'teachers'
            ? 'bg-amber-700 text-white'
            : 'bg-white/80 text-gray-700 hover:bg-gray-100'
        "
      >
        <i class="fa-solid fa-chalkboard-user mr-2"></i>教师
      </button>
      <button
        @click="scrollTo('labs')"
        class="px-3 py-2 rounded-lg shadow border border-amber-100 transition-colors"
        :class="
          activeId === 'labs'
            ? 'bg-amber-700 text-white'
            : 'bg-white/80 text-gray-700 hover:bg-gray-100'
        "
      >
        <i class="fa-solid fa-flask mr-2"></i>实验室
      </button>
      <button
        @click="scrollTo('forum')"
        class="px-3 py-2 rounded-lg shadow border border-amber-100 transition-colors"
        :class="
          activeId === 'forum'
            ? 'bg-amber-700 text-white'
            : 'bg-white/80 text-gray-700 hover:bg-gray-100'
        "
      >
        <i class="fa-solid fa-comments mr-2"></i>论坛
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'
import collegesData from '@/components/college/colleges-data.json'
import CommentForm from '@/components/college/CommentForm.vue'
import CommentItem from '@/components/college/CommentItem.vue'

// 路由相关
const route = useRoute()
const router = useRouter()

// 当前学院
const collegeId = computed(() => parseInt(route.params.id as string))
const college = computed(() => collegesData.find((c) => c.id === collegeId.value))

// 评论与用户接口定义
interface Comment {
  id: number
  collegeId: number
  userId: number
  userName: string
  parentId?: number
  content: string
  createdAt: string
  likeCount: number
  isLiked: boolean
  replies?: Comment[]
}

// 响应式数据
const comments = ref<Comment[]>([])
const currentUserId = ref<number | undefined>()

const activeId = ref('introduction')
const sectionIds = ['introduction', 'teachers', 'labs', 'forum']
let observer: IntersectionObserver | null = null

// 滚动到指定区域
const scrollTo = (id: string) => {
  const el = document.getElementById(id)
  el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

// 获取评论列表
const fetchComments = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.COLLEGE_COMMENTS(collegeId.value)), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      const data = await response.json()
      // 处理从后端获取的评论数据，包含avatarUrl字段
      comments.value = data
    }
  } catch (error) {
    console.error('获取评论失败:', error)
  }
}

// 获取当前用户ID
const getCurrentUserId = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return

    const response = await fetch(getApiUrl(API_ENDPOINTS.USER_INFO), {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      const data = await response.json()
      currentUserId.value = data?.userId
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 初始化
onMounted(async () => {
  // 加载数据
  await Promise.all([fetchComments(), getCurrentUserId()])

  // 初始化交叉观察器，监听section可见性
  const options = {
    root: null, // 使用视口作为根容器
    rootMargin: '-20% 0px -60% 0px', // 调整触发区域（视觉中心）
    threshold: 0,
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id')
        if (id && sectionIds.includes(id)) {
          activeId.value = id
        }
      }
    })
  }, options)

  // 监听所有section
  sectionIds.forEach((id) => {
    const el = document.getElementById(id)
    if (el) observer?.observe(el)
  })
})

// 组件卸载时清理观察器，避免内存泄漏
onUnmounted(() => {
  if (observer) {
    sectionIds.forEach((id) => {
      const el = document.getElementById(id)
      if (el) observer?.unobserve(el)
    })
    observer.disconnect()
    observer = null
  }
})
</script>

<style scoped>
/* 滚动偏移量：避免标题被顶部遮挡 */
.scroll-mt-32 {
  scroll-margin-top: 8rem;
}

/* 平滑滚动 */
section {
  scroll-behavior: smooth;
}

/* 自定义背景色 */
.bg-parchment {
  background-color: #f8f4e9;
}

.bg-amber-50 {
  background-color: #fffbeb;
}

.bg-amber-100 {
  background-color: #fef3c7;
}

.text-amber-200 {
  color: #fcd34d;
}

.text-amber-600 {
  color: #d97706;
}

.text-amber-700 {
  color: #b45309;
}

.text-amber-800 {
  color: #92400e;
}

.text-amber-900 {
  color: #78350f;
}

.border-amber-100 {
  border-color: #fef3c7;
}

.border-amber-200 {
  border-color: #fcd34d;
}
</style>
