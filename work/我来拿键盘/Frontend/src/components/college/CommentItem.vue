<template>
  <div class="comment-item">
    <!-- 评论主体 -->
    <div class="flex gap-3 mb-3">
      <!-- 头像 -->
      <div class="w-10 h-10 rounded-full overflow-hidden flex-shrink-0 border-2 border-amber-200">
        <img
          v-if="props.comment.avatarUrl"
          :src="getFullAvatarUrl(props.comment.avatarUrl)"
          :alt="`${props.comment.userName}的头像`"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full bg-amber-200 flex items-center justify-center">
          <i class="fa-solid fa-user text-amber-700"></i>
        </div>
      </div>

      <!-- 评论内容 -->
      <div class="flex-1 bg-gray-50 rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="font-semibold text-gray-800">{{ props.comment.userName }}</span>
          <span class="text-xs text-gray-500">{{ formatTime(props.comment.createdAt) }}</span>
        </div>

        <p class="text-gray-700 mb-3">
          <!-- 回复标识 -->
          <span v-if="props.comment.parentId" class="text-amber-600">@回复：</span>
          {{ props.comment.content }}
        </p>

        <!-- 操作按钮 -->
        <div class="flex items-center gap-4 text-sm">
          <button
            @click="handleLike"
            :class="props.comment.isLiked ? 'text-red-500' : 'text-gray-500'"
            class="hover:text-red-500 transition-colors flex items-center gap-1"
          >
            <i :class="props.comment.isLiked ? 'fa-solid fa-heart' : 'fa-regular fa-heart'"></i>
            <span>{{ props.comment.likeCount || '点赞' }}</span>
          </button>

          <button
            @click="showReplyForm = !showReplyForm"
            class="text-gray-500 hover:text-amber-600 transition-colors"
          >
            <i class="fa-solid fa-reply mr-1"></i>回复
          </button>

          <!-- 展开/收起回复按钮 -->
          <button
            v-if="props.comment.replies && props.comment.replies.length > 0"
            @click="isRepliesExpanded = !isRepliesExpanded"
            class="text-gray-500 hover:text-amber-600 transition-colors flex items-center gap-1"
          >
            <i
              :class="
                isRepliesExpanded ? 'fa-solid fa-chevron-up mr-1' : 'fa-solid fa-chevron-down mr-1'
              "
            ></i>
            {{ isRepliesExpanded ? '收起回复' : `查看${props.comment.replies.length}条回复` }}
          </button>

          <button
            v-if="canDelete"
            @click="handleDelete"
            class="text-gray-500 hover:text-red-600 transition-colors"
          >
            <i class="fa-solid fa-trash mr-1"></i>删除
          </button>
        </div>

        <!-- 回复表单 -->
        <div v-if="showReplyForm" class="mt-3">
          <CommentForm
            :college-id="props.comment.collegeId"
            :parent-id="props.comment.id"
            :placeholder="`回复 @${props.comment.userName}`"
            @submitted="handleReplySubmitted"
          />
        </div>
      </div>
    </div>

    <!-- 嵌套回复 - 可展开/收起，有宽度缩进 -->
    <div
      v-if="isRepliesExpanded && props.comment.replies && props.comment.replies.length > 0"
      class="ml-4 pl-4 border-l-2 border-gray-100 space-y-3 mt-3"
    >
      <!-- 显示当前加载的回复 -->
      <div v-for="reply in displayedReplies" :key="reply.id" class="reply-item">
        <!-- 回复内容 -->
        <div class="flex gap-3">
          <!-- 头像 -->
          <div class="w-9 h-9 rounded-full overflow-hidden flex-shrink-0 border-2 border-amber-200">
            <img
              v-if="reply.avatarUrl"
              :src="getFullAvatarUrl(reply.avatarUrl)"
              :alt="`${reply.userName}的头像`"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-amber-200 flex items-center justify-center">
              <i class="fa-solid fa-user text-amber-700 text-sm"></i>
            </div>
          </div>

          <!-- 回复内容区 -->
          <div class="flex-1 bg-gray-50 rounded-lg p-3">
            <div class="flex items-center justify-between mb-1">
              <span class="font-semibold text-gray-800 text-sm">{{ reply.userName }}</span>
              <span class="text-xs text-gray-500">{{ formatTime(reply.createdAt) }}</span>
            </div>

            <p class="text-gray-700 mb-2 text-sm">
              <span class="text-amber-600">@{{ props.comment.userName }}：</span>
              {{ reply.content }}
            </p>

            <!-- 回复操作按钮 -->
            <div class="flex items-center gap-4 text-xs">
              <button
                @click="handleReplyLike(reply)"
                :class="reply.isLiked ? 'text-red-500' : 'text-gray-500'"
                class="hover:text-red-500 transition-colors flex items-center gap-1"
              >
                <i
                  :class="
                    reply.isLiked ? 'fa-solid fa-heart text-xs' : 'fa-regular fa-heart text-xs'
                  "
                ></i>
                <span>{{ reply.likeCount || '点赞' }}</span>
              </button>

              <button
                v-if="currentUserId === reply.userId"
                @click="handleReplyDelete(reply)"
                class="text-gray-500 hover:text-red-600 transition-colors"
              >
                <i class="fa-solid fa-trash text-xs mr-1"></i>删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载更多按钮 -->
      <div v-if="hasMoreReplies" class="text-center mt-2">
        <button
          @click="loadMoreReplies"
          class="text-amber-600 hover:text-amber-800 text-sm transition-colors"
          :disabled="isLoading"
        >
          <i v-if="isLoading" class="fa-solid fa-spinner fa-spin mr-1"></i>
          {{ isLoading ? '加载中...' : '加载更多回复' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { getApiUrl, getStaticUrl, API_ENDPOINTS, STATIC_ENDPOINTS } from '@/config/api'
import CommentForm from './CommentForm.vue'

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
  avatarUrl?: string
  replies?: Comment[]
}

const props = defineProps<{
  comment: Comment
  currentUserId?: number
}>()

const emit = defineEmits<{
  deleted: []
  liked: []
}>()

const showReplyForm = ref(false)
const isRepliesExpanded = ref(false)
const displayedRepliesCount = ref(5) // 默认显示5条回复
const isLoading = ref(false)

// 计算当前显示的回复
const displayedReplies = computed(() => {
  if (!props.comment.replies) return []
  return props.comment.replies.slice(0, displayedRepliesCount.value)
})

// 是否还有更多回复
const hasMoreReplies = computed(() => {
  return props.comment.replies && props.comment.replies.length > displayedRepliesCount.value
})

// 处理头像URL，确保是完整的后端URL
const getFullAvatarUrl = (url: string) => {
  console.log('CommentItem - 原始头像URL:', url)
  // 检查是否是完整的HTTP/HTTPS链接
  if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
    console.log('CommentItem - 使用完整URL:', url)
    return url
  }
  // 如果不是完整链接，添加后端基础URL
  const fullUrl = url ? getApiUrl(url) : getStaticUrl(STATIC_ENDPOINTS.AVATAR_DEFAULT)
  console.log('CommentItem - 构建完整URL:', fullUrl)
  return fullUrl
}

const canDelete = computed(() => {
  return props.currentUserId && props.currentUserId === props.comment.userId
})

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

const handleLike = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.COLLEGE_COMMENT_LIKE(props.comment.id)), {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      emit('liked')
    }
  } catch (error) {
    console.error('Failed to toggle like:', error)
  }
}

const handleDelete = async () => {
  if (!confirm('确定要删除这条评论吗？')) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      getApiUrl(API_ENDPOINTS.COLLEGE_COMMENT_DELETE(props.comment.id)),
      {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    if (response.ok) {
      emit('deleted')
    }
  } catch (error) {
    console.error('Failed to delete comment:', error)
  }
}

const handleReplySubmitted = () => {
  showReplyForm.value = false
  emit('deleted') // 触发刷新
}

// 处理回复的点赞
const handleReplyLike = async (reply: Comment) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.COLLEGE_COMMENT_LIKE(reply.id)), {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      emit('liked')
    }
  } catch (error) {
    console.error('Failed to toggle reply like:', error)
  }
}

// 处理回复的删除
const handleReplyDelete = async (reply: Comment) => {
  if (!confirm('确定要删除这条回复吗？')) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.COLLEGE_COMMENT_DELETE(reply.id)), {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (response.ok) {
      emit('deleted')
    }
  } catch (error) {
    console.error('Failed to delete reply:', error)
  }
}

// 加载更多回复
const loadMoreReplies = async () => {
  if (isLoading.value || !hasMoreReplies.value) return

  isLoading.value = true
  try {
    // 模拟加载延迟
    await new Promise((resolve) => setTimeout(resolve, 500))
    // 增加显示的回复数量
    displayedRepliesCount.value += 5
  } catch (error) {
    console.error('Failed to load more replies:', error)
  } finally {
    isLoading.value = false
  }
}
</script>
