<template>
  <div class="home-container">
    <Header :userName="username" />
    <main class="main-content">
      <!-- 形体评估测试模块 -->
      <section class="evaluation-section">
        <!-- <h2 class="section-title">形体评估测试</h2> -->

        <!-- 初始对话框（禁用状态） -->
        <div class="initial-dialog" :class="{ disabled: !chatEnabled }">
          <div class="dialog-header">
            <h3>形体评估助手</h3>
            <span class="status-indicator" :class="{ active: chatEnabled }">
              {{ chatEnabled ? '评估' : '离线' }}
            </span>
          </div>
          <div class="dialog-content" ref="messageList" @scroll="handleMessageListScroll">

            <div class="message-list">
              <div class="message bot-message" v-if="!chatEnabled">
                <div class="avatar">🤖</div>
                <div class="bubble">
                  <p>请先上传视频进行评估</p>
                </div>
              </div>
              <div
                v-for="(message, index) in chatMessages"
                :key="index"
                class="message"
                :class="message.type"
              >
                <div class="avatar">{{ message.type === 'user-message' ? '👤' : '🤖' }}</div>
                <div class="bubble">
                  <div class="markdown-content" v-html="renderMarkdown(message.content)"></div>
                  <!-- <p>{{ message.content }}</p> -->
                  <span class="timestamp">{{ message.timestamp }}</span>
                </div>
              </div>
              <div class="typing-indicator" v-if="isTyping">
                <div class="avatar">🤖</div>
                <div class="bubble">
                  <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="dialog-input">
            <input
              type="text"
              v-model="userInput"
              placeholder="输入您的问题..."
              :disabled="!chatEnabled || isWaitingResponse"
              @keyup.enter="sendMessage"
            />
            <button
              class="send-btn"
              @click="sendMessage"
              :disabled="!chatEnabled || isWaitingResponse || !userInput.trim()"
            >
              {{ isWaitingResponse ? '发送中...' : '发送' }}
            </button>
          </div>
        </div>

        <!-- 上传按钮 -->
        <div class="upload-button-container">
          <button class="btn-primary upload-btn" @click="showUploadModal" :disabled="isWaitingResponse">
            {{ hasUploadedVideos ? '重新上传视频' : '开始评估' }}
          </button>
          <div class="upload-status" v-if="hasUploadedVideos">
            <span class="status-text">已上传 {{ uploadedVideosCount }}/2 个视频</span>
            <button class="clear-btn" @click="clearUploadedVideos" :disabled="isWaitingResponse">清除</button>
          </div>
        </div>
      </section>

      <section class="video-section">
        <h2 class="section-title">精选教学视频</h2>
        <div class="video-grid">
          <div
            v-for="video in teachingVideos"
            :key="video.id"
            class="video-card"
            @click="previewVideo(video)"
          >
            <div class="video-thumbnail">
              <img :src="API_BASE_URL+video.thumbnail" :alt="video.title" />
              <div class="play-overlay">
                <i class="play-icon">▶</i>
              </div>
            </div>
            <div class="video-info">
              <h3 class="video-title">{{ video.title }}</h3>
              <p class="video-duration">{{ video.duration }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 视频上传模态框 -->
    <div class="modal-overlay" v-if="showUploadModalFlag" @click="closeUploadModal">
      <div class="modal-content upload-modal" @click.stop>
        <div class="modal-header">
          <h3>上传评估视频</h3>
          <button class="close-btn" @click="closeUploadModal">×</button>
        </div>
        <div class="modal-body">
          <p class="upload-instruction">请上传正面和侧面两个角度的视频以获得准确评估</p>

          <div class="video-upload-grid">
            <div class="video-upload-item">
              <h4>正面视频</h4>
              <div
                class="upload-area"
                :class="{ 'has-file': uploadedVideos.front }"
                @click="triggerFileInput('front')"
                @drop="handleDrop($event, 'front')"
                @dragover.prevent
              >
                <div class="upload-icon">
                  <i class="icon" v-if="!uploadedVideos.front">📹</i>
                  <i class="icon" v-else>✅</i>
                </div>
                <p class="upload-text" v-if="!uploadedVideos.front">点击或拖拽正面视频</p>
                <p class="upload-text" v-else>
                  {{ uploadedVideos.front.name }}
                </p>
                <p class="upload-hint">支持MP4、MOV、AVI格式</p>
              </div>
              <input
                type="file"
                ref="frontFileInput"
                @change="handleFileSelect($event, 'front')"
                accept="video/*"
                class="file-input"
              />
            </div>

            <div class="video-upload-item">
              <h4>侧面视频</h4>
              <div
                class="upload-area"
                :class="{ 'has-file': uploadedVideos.side }"
                @click="triggerFileInput('side')"
                @drop="handleDrop($event, 'side')"
                @dragover.prevent
              >
                <div class="upload-icon">
                  <i class="icon" v-if="!uploadedVideos.side">📹</i>
                  <i class="icon" v-else>✅</i>
                </div>
                <p class="upload-text" v-if="!uploadedVideos.side">点击或拖拽侧面视频</p>
                <p class="upload-text" v-else>
                  {{ uploadedVideos.side.name }}
                </p>
                <p class="upload-hint">支持MP4、MOV、AVI格式</p>
              </div>
              <input
                type="file"
                ref="sideFileInput"
                @change="handleFileSelect($event, 'side')"
                accept="video/*"
                class="file-input"
              />
            </div>
          </div>

          <div class="upload-progress" v-if="uploading">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <p class="progress-text">上传中... {{ uploadStatus }}%</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeUploadModal">取消</button>
          <button class="btn-primary" @click="submitVideos" :disabled="!canSubmit || uploading">
            {{ uploading ? '上传中...' : '开始评估' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 视频预览模态框 -->
    <div class="modal-overlay" v-if="previewVideoData" @click="closePreview">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ previewVideoData.title }}</h3>
          <button class="close-btn" @click="closePreview">×</button>
        </div>
        <div class="video-player">

          <video :src="previewVideoData.url" controls ref="videoPlayer" :key="videoKey"></video>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="toggleFullscreen">全屏观看</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
export default {
  name: 'Home' // 必须与 keep-alive include 中的字符串一致
}
</script>

<script setup lang="ts">
import './styles/Home.css'

import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import type{ TeachingVideo } from '@/types/video'
import { videoApi } from '@/utils/video'
import Header from './HeaderComponent.vue'
import axios from 'axios' // 导入 axios
import type { AxiosProgressEvent } from 'axios'
import type { ComponentPropsMap } from '@/types/main'
import MarkdownIt from 'markdown-it'

const videoKey = ref(0)
const props = withDefaults(defineProps<ComponentPropsMap['home']>(),{
  options: ()=>({
    html: true,
    linkify: true,
    typographer: true,
    breaks: true,
  }),
  username: 'test'
})



const md = new MarkdownIt(props.options)

const renderMarkdown = (content: string) => {
  return md.render(content || '')
}



// 文件上传相关
const frontFileInput = ref<HTMLInputElement | null>(null)
const sideFileInput = ref<HTMLInputElement | null>(null)
const showUploadModalFlag = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref('')
const uploadedVideos = reactive({
  front: null as File | null,
  side: null as File | null,
})

// 评估结果相关
const evaluationResult = ref<EvaluationResult | null>(null)
const chatEnabled = ref(false)

const isReupload = ref(false)

// 聊天相关
const chatMessages = ref<ChatMessage[]>([])
const userInput = ref('')
const isWaitingResponse = ref(false)
const isTyping = ref(false)

// 教学视频相关
const teachingVideos = ref<TeachingVideo[]>([])
const previewVideoData = ref<TeachingVideo | null>(null)
const videoPlayer = ref<HTMLVideoElement | null>(null)

// 类型定义
interface EvaluationResult {
  message: string
}



interface ChatMessage {
  type: 'user-message' | 'bot-message'
  content: string
  timestamp: string
}

// 计算属性
const hasUploadedVideos = computed(() => {
  return uploadedVideos.front !== null || uploadedVideos.side !== null
})

const uploadedVideosCount = computed(() => {
  let count = 0
  if (uploadedVideos.front) count++
  if (uploadedVideos.side) count++
  return count
})

const canSubmit = computed(() => {
  return uploadedVideos.front !== null && uploadedVideos.side !== null
})

// // 处理上传按钮点击
// const handleUploadClick = () => {
//   if (evaluationResult.value) {
//     isReupload.value = true
//     resetContext()
//   }
//   showUploadModalFlag.value = true
// }

// 重置上下文
const resetContext = () => {
  chatEnabled.value = false
  chatMessages.value = []

  userInput.value = ''
  isWaitingResponse.value = false
  isTyping.value = false
  result.value = ''
  flag.value = true
}

// 显示上传模态框
const showUploadModal = () => {
  showUploadModalFlag.value = true
}

// 关闭上传模态框
const closeUploadModal = () => {
  showUploadModalFlag.value = false
  if (isReupload.value && evaluationResult.value) {
    chatEnabled.value = true
  }
  isReupload.value = false
}
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
// 清除已上传的视频
const clearUploadedVideos = async() => {


  uploadedVideos.front = null
  uploadedVideos.side = null
  evaluationResult.value = null
  chatEnabled.value = false
  chatMessages.value = []
  isReupload.value = false
  resetContext()


  await axios.get(`${API_BASE_URL}/api/clear`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
      },
    })


}

// 触发文件选择
const triggerFileInput = (type: 'front' | 'side') => {
  if (type === 'front' && frontFileInput.value) {
    frontFileInput.value.click()
  } else if (type === 'side' && sideFileInput.value) {
    sideFileInput.value.click()
  }
}

// 处理文件选择
const handleFileSelect = (event: Event, type: 'front' | 'side') => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    if (file) {
      // 验证文件类型和大小
      if (!file.type.startsWith('video/')) {
        alert('请上传视频文件')
        return
      }

      if (file.size > 100 * 1024 * 1024) {
        // 100MB
        alert('文件大小不能超过100MB')
        return
      }

      uploadedVideos[type] = file
    }
  }
}

// 处理拖放上传
const handleDrop = (event: DragEvent, type: 'front' | 'side') => {
  event.preventDefault()
  if (event.dataTransfer && event.dataTransfer.files.length > 0) {
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('video/')) {
      // 验证文件大小
      if (file.size > 100 * 1024 * 1024) {
        alert('文件大小不能超过100MB')
        return
      }
      uploadedVideos[type] = file
    }
  }
}


const result=ref('')
const flag=ref(true)

// 提交视频进行评估
const submitVideos = async () => {
  if (!canSubmit.value) return
    if (evaluationResult.value) {
    isReupload.value = true
    resetContext()
  }
  showUploadModalFlag.value = true
  // 如果是重新上传，先清除之前的评估结果
  if (isReupload.value) {

    evaluationResult.value = null
    resetContext()
    await axios.get(`${API_BASE_URL}/api/clear`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
      },
    })

  }

  uploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = '准备上传...'

  try {
    // 创建 FormData
    const formData = new FormData()
    if (uploadedVideos.front) {
      formData.append('front_video', uploadedVideos.front)
    }
    if (uploadedVideos.side) {
      formData.append('side_video', uploadedVideos.side)
    }
    const token = localStorage.getItem('token') || ''

    // 发送到 Flask 服务器
    const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`,
      },

      onUploadProgress: (progressEvent: AxiosProgressEvent) => {
        if (progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadProgress.value = progress
          uploadStatus.value = `上传中... ${progress}%`
        }
      },
    })

    // 处理服务器响应
    if (response.data.success) {
      uploadStatus.value = '分析视频中...'
      uploadProgress.value = 100
      setTimeout(()=>{

      },500)
      // 等待分析完成
      await waitForAnalysis(response.data.task_id)
    } else {
      throw new Error(response.data.message || '上传失败')
    }
  } catch (error: unknown) {
    console.error('上传失败:', error)
    uploadStatus.value = '上传失败，请重试'
    if (error instanceof Error){
        addBotMessage(
        '视频上传失败：' + (error.message || '请检查网络连接后重试'),
      )
    }else{
      addBotMessage(
        '视频上传失败：' + ( '请检查网络连接后重试'),
      )
    }


    // 重置上传状态
    setTimeout(() => {
      uploading.value = false
      uploadProgress.value = 0
      uploadStatus.value = ''
    }, 3000)
  }
}

// 等待分析完成
const waitForAnalysis = async (taskId: string) => {
  try {
    uploadStatus.value = '分析视频中...'

    // 轮询获取分析结果
    const checkResult = async (): Promise<void> => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/evaluate/result/${taskId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
            },
          }
        )
        if (response.data.status === 'completed') {
          // 分析完成，获取结果
          evaluationResult.value = response.data.result
          chatEnabled.value = true

          // 重置上传状态
          uploading.value = false
          uploadProgress.value = 0
          uploadStatus.value = ''
          showUploadModalFlag.value = false
          isReupload.value = false


          sendMessage()

        } else if (response.data.status === 'processing') {
          // 仍在处理中，继续等待
          setTimeout(checkResult, 2000)
        } else {
          // 处理失败
          throw new Error(response.data.message || '分析失败')
        }
      } catch (error) {
        console.error('轮询错误:', error)
        throw error
      }
    }

    // 开始轮询
    await checkResult()
  } catch (error: unknown) {
    console.error('分析失败:', error)
    uploadStatus.value = '分析失败，请重试'
    if (error instanceof Error){
        addBotMessage(
        '视频分析失败：' + (error.message || '请稍后重试'),
      )
    }else{
      addBotMessage(
        '视频分析失败：' + ('请稍后重试'),
      )
    }


    // 重置上传状态
    setTimeout(() => {
      uploading.value = false
      uploadProgress.value = 0
      uploadStatus.value = ''
    }, 3000)
  }
}



// 添加机器人消息
const addBotMessage = (content: string) => {
  chatMessages.value.push({
    type: 'bot-message',
    content,
    timestamp: new Date().toLocaleTimeString(),
  })
}

// 添加用户消息
const addUserMessage = (content: string) => {
  chatMessages.value.push({
    type: 'user-message',
    content,
    timestamp: new Date().toLocaleTimeString(),
  })
}

const messageList = ref<HTMLElement | null>(null)

let userHasScrolled = false
let lastScrollTop = 0
const scrollToBottom = () => {
  nextTick(() => {
    // 否则滚动到消息列表底部
    if (messageList.value) {
      messageList.value.scrollTo({
        top: messageList.value.scrollHeight,
        behavior: 'smooth',
      })
    }
  })
}
const isNearBottom = (threshold = 100) => {
  if (!messageList.value) return true

  const { scrollTop, scrollHeight, clientHeight } = messageList.value
  return scrollHeight - scrollTop - clientHeight <= threshold
}

// 智能滚动函数
const smartScrollToBottom = () => {
  setTimeout(() => {
    if (!userHasScrolled || isNearBottom()) {
      scrollToBottom()
    }
  }, 1000)
}

// 监听用户滚动行为
const handleMessageListScroll = () => {
  if (messageList.value) {
    const { scrollTop, scrollHeight, clientHeight } = messageList.value

    // 如果用户向上滚动，标记为手动滚动
    if (scrollTop < lastScrollTop) {
      userHasScrolled = true
    }

    // 如果用户滚动到底部附近，重置手动滚动标记
    if (scrollHeight - scrollTop - clientHeight < 50) {
      userHasScrolled = false
    }

    lastScrollTop = scrollTop
  }
}

// 重置滚动状态（当新消息发送时）
const resetScrollState = () => {
  userHasScrolled = false
}

// chatEnabled.value = true
// 发送消息 - 流式响应版本


const save_history= async() => {
  setTimeout(async() => {
    try {

    const token = localStorage.getItem('token') || ''
    const response = await fetch(`${API_BASE_URL}/api/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message: result.value,
      }),
    })

    if (!response.ok) {
      throw new Error('网络响应不正常')
    }
    await response.json()
  } catch (error) {
    console.error('保存历史记录失败:', error)
  }


  }, 1000)


}

const sendMessage = async () => {

  if ( isWaitingResponse.value || !chatEnabled.value|| !evaluationResult.value) return

  let message = ''
  if (userInput.value.trim()){
    message = userInput.value.trim()
    userInput.value = ''
    resetScrollState()
    addUserMessage(message)
  }else if (evaluationResult.value) {
    message = evaluationResult.value.message
  }
  isWaitingResponse.value = true
  isTyping.value = true

  try {
    // 发送消息到服务器
    const token = localStorage.getItem('token') || ''
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message: message,
        // 可以添加评估结果作为上下文

      }),
    })

    if (!response.ok) {
      throw new Error('网络响应不正常')
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('无法读取响应流')
    }

    // 添加初始机器人消息
    const botMessageIndex = chatMessages.value.length
    // addBotMessage('')
    addBotMessage('')

    // 读取流式数据
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      // 将接收到的数据添加到消息中
      const text = new TextDecoder().decode(value)

      const lines = text.split('\n').filter((line) => line.trim() !== '')
      for (const line of lines) {
        let data
        try {
          data = JSON.parse(line.substring(6).trim()) // 去掉 "data:" 前缀
        } catch (e) {
          console.error('解析数据失败:', e)
          console.log('原始数据:', text)
          continue
        }

        if (flag.value){
          result.value += data.content
        }
        if (chatMessages.value[botMessageIndex]) {
          chatMessages.value[botMessageIndex].content += data.content
          isTyping.value = false
        } else {
          // 如果消息不存在，创建新的消息
          addBotMessage(data.content)
        }
        smartScrollToBottom()
      }
    }

    save_history()

  } catch (error: unknown) {
    console.error('发送消息失败:', error)
    addBotMessage('抱歉，我暂时无法回复，请稍后重试。')
  } finally {
    isWaitingResponse.value = false
    isTyping.value = false

    flag.value=false
  }
}

// 预览视频
const previewVideo = (video: TeachingVideo) => {
  previewVideoData.value = {
    ...video,
    url:API_BASE_URL+video.url
  }

  videoKey.value+=1
}

// 关闭预览
const closePreview = () => {
  previewVideoData.value = null
}



// 切换全屏
const toggleFullscreen = () => {
  if (videoPlayer.value) {
    if (videoPlayer.value.requestFullscreen) {
      videoPlayer.value.requestFullscreen()
    }
  }
}


// 获取教学视频列表
const fetchTeachingVideos = async () => {
  try {

    const token=localStorage.getItem('token')||''
    const data=await videoApi.fetch_all_videos(token)
    const mockVideos: TeachingVideo[]=data.data
    teachingVideos.value = mockVideos
  } catch (error) {
    console.error('获取教学视频失败:', error)
  }
}


// 组件挂载后获取教学视频
onMounted(() => {
  fetchTeachingVideos()

})
</script>

<style scoped>

</style>
