<template>
  <div class="media-management">
    <!-- 头部标题和统计 -->
    <div class="header">
      <h3>媒体内容管理</h3>
      <div class="stats">
        <span class="video-count">视频总数: {{ videos.length }}</span>
        <span class="total-size">总大小: {{ formatFileSize(totalSize) }}</span>
      </div>
    </div>

    <!-- 上传视频区域 -->
    <div class="upload-section">
      <div class="upload-header">
        <h4>上传视频</h4>
        <span class="upload-tip">支持 MP4, AVI, MOV 等格式，最大 2GB</span>
      </div>
      
      <div class="upload-form">
        <!-- 视频名称输入 -->
        <div class="form-group">
          <label for="videoName" class="form-label">
            视频名称 <span class="required">*</span>
          </label>
          <input
            id="videoName"
            v-model="uploadForm.name"
            type="text"
            placeholder="请输入视频名称"
            class="form-input"
            :class="{ error: formErrors.name }"
            @input="clearError('name')"
          />
          <div v-if="formErrors.name" class="error-message">{{ formErrors.name }}</div>
        </div>

        <!-- 视频批注输入 -->
        <div class="form-group">
          <label for="videoAnnotation" class="form-label">视频批注</label>
          <textarea
            id="videoAnnotation"
            v-model="uploadForm.annotation"
            placeholder="请输入视频批注或描述信息"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>

        <!-- 文件选择 -->
        <div class="form-group">
          <label for="videoFile" class="form-label">
            选择视频文件 <span class="required">*</span>
          </label>
          <div class="file-upload-area" 
               :class="{ 'drag-over': dragOver, 'has-file': uploadForm.file }"
               @click="triggerFileInput"
               @drop="handleFileDrop"
               @dragover.prevent="handleDragOver"
               @dragleave="dragOver = false">
            <div class="file-upload-content">
              <div class="upload-icon">📁</div>
              <template v-if="!uploadForm.file">
                <div class="upload-text">点击选择或拖拽视频文件到此区域</div>
                <div class="upload-hint">最大支持 2GB，支持 MP4, AVI, MOV 等格式</div>
              </template>
              <template v-else>
                <div class="file-info">
                  <div class="file-name">{{ uploadForm.file.name }}</div>
                  <div class="file-size">{{ formatFileSize(uploadForm.file.size) }}</div>
                </div>
              </template>
            </div>
            <input
              id="videoFile"
              ref="fileInput"
              type="file"
              accept="video/*"
              @change="handleFileSelect"
              class="file-input-hidden"
            />
          </div>
          <div v-if="formErrors.file" class="error-message">{{ formErrors.file }}</div>
        </div>

        <!-- 上传按钮 -->
        <div class="upload-actions">
          <button
            :disabled="!canUpload || uploading"
            @click="uploadVideo"
            class="upload-btn"
            :class="{ loading: uploading }"
          >
            <span v-if="uploading" class="loading-spinner"></span>
            {{ uploading ? '上传中...' : '上传至服务器' }}
          </button>
          <button 
            @click="resetUploadForm" 
            class="cancel-btn"
            :disabled="uploading">
            重置
          </button>
        </div>
      </div>
    </div>

    <!-- 视频列表 -->
    <div class="video-list-section">
      <div class="section-header">
        <h4>视频列表 ({{ videos.length }})</h4>
        <div class="section-actions">
          <button 
            @click="refreshVideos" 
            class="refresh-btn"
            :disabled="loading">
            {{ loading ? '刷新中...' : '刷新列表' }}
          </button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>加载视频列表中...</span>
      </div>

      <!-- 视频列表内容 -->
      <div v-else class="video-list">
        <div
          v-for="video in videos"
          :key="video.id"
          class="video-item"
          :class="{ deleting: deletingId === video.id }"
        >
          <div class="video-preview">
            <div class="video-icon">🎬</div>
            <div class="video-duration" v-if="video.duration">
              {{ formatDuration(video.duration) }}
            </div>
          </div>
          
          <div class="video-info">
            <div class="video-name">{{ video.name }}</div>
            <div class="video-annotation" :title="video.annotation">
              {{ video.annotation || '无批注' }}
            </div>
            <div class="video-meta">
              <span class="upload-time">
                <span class="meta-label">上传时间:</span>
                {{ formatTime(video.uploadTime) }}
              </span>
              <span class="video-size">
                <span class="meta-label">文件大小:</span>
                {{ formatFileSize(video.size) }}
              </span>
              <!-- <span v-if="video.duration" class="video-duration">
                <span class="meta-label">时长:</span>
                {{ formatDuration(video.duration) }}
              </span> -->
            </div>
          </div>
          
          <div class="video-actions">
            <button
              v-if="video.url"
              @click="previewVideo(video)"
              class="preview-btn"
              title="预览视频"
            >
              预览
            </button>
            <button
              @click="deleteVideo(video.id)"
              class="delete-btn"
              :disabled="deletingId === video.id"
              title="删除视频"
            >
              <span v-if="deletingId === video.id" class="deleting-spinner"></span>
              {{ deletingId === video.id ? '删除中...' : '删除' }}
            </button>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="videos.length === 0" class="empty-state">
          <div class="empty-icon">📹</div>
          <div class="empty-text">暂无视频文件</div>
          <div class="empty-hint">上传第一个视频开始管理您的媒体内容</div>
        </div>
      </div>
    </div>

    <!-- 视频预览模态框 -->
    <div v-if="previewVideoData" class="video-preview-modal" @click="closePreview">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ previewVideoData.name }}</h3>
          <button @click="closePreview" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <video 
            v-if="previewVideoData.url"
            :src="previewVideoData.url" 
            controls
            class="preview-video"
          >
            您的浏览器不支持视频播放
          </video>
          <div v-else class="no-preview">
            视频预览不可用
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

// ========== 接口定义 ==========
interface VideoItem {
  id: number
  name: string
  annotation: string
  uploadTime: string
  size: number
  url?: string
  duration?: number
}

interface UploadForm {
  name: string
  annotation: string
  file: File | null
}

interface FormErrors {
  name?: string
  file?: string
}

// ========== Props & Emits ==========
interface Props {
  videos: VideoItem[]
  loading?: boolean
}

interface Emits {
  (e: 'video-upload', formData: { name: string; annotation: string; file: File }): void
  (e: 'video-delete', videoId: number): void
  (e: 'refresh'): void
}

const props = withDefaults(defineProps<Props>(), {
    videos: () => [],
  loading: false
})

const emit = defineEmits<Emits>()

// ========== 响应式数据 ==========
const uploadForm = ref<UploadForm>({
  name: '',
  annotation: '',
  file: null
})

const formErrors = ref<FormErrors>({})
const uploading = ref(false)
const deletingId = ref<number | null>(null)
const dragOver = ref(false)
const previewVideoData = ref<VideoItem | null>(null)
const fileInput = ref<HTMLInputElement>()

// ========== 计算属性 ==========
const canUpload = computed(() => {
  return uploadForm.value.name.trim() && 
         uploadForm.value.file && 
         !uploading.value &&
         Object.keys(formErrors.value).length === 0
})

const totalSize = computed(() => {
  return props.videos.reduce((total, video) => total + video.size, 0)
})

// ========== 方法定义 ==========

/**
 * 触发文件选择
 */
const triggerFileInput = () => {
  fileInput.value?.click()
}

/**
 * 处理文件选择
 */
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    validateAndSetFile(target.files[0])
  }
}

/**
 * 处理文件拖放
 */
const handleFileDrop = (event: DragEvent) => {
  event.preventDefault()
  dragOver.value = false
  
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    validateAndSetFile(event.dataTransfer.files[0])
  }
}

/**
 * 处理拖拽悬停
 */
const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  dragOver.value = true
}

/**
 * 验证并设置文件
 */
const validateAndSetFile = (file: File) => {
  clearError('file')
  
  // 验证文件类型
  const allowedTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo']
  if (!allowedTypes.some(type => file.type.includes(type.replace('video/', '')))) {
    formErrors.value.file = '请选择有效的视频文件 (MP4, AVI, MOV 等格式)'
    return
  }
  
  // 验证文件大小 (2GB)
  const maxSize = 2 * 1024 * 1024 * 1024
  if (file.size > maxSize) {
    formErrors.value.file = '文件大小不能超过 2GB'
    return
  }
  
  uploadForm.value.file = file
  
  // 如果还没有设置名称，使用文件名作为默认名称
  if (!uploadForm.value.name.trim()) {
    uploadForm.value.name = file.name.replace(/\.[^/.]+$/, "")
  }
}

/**
 * 清除错误信息
 */
const clearError = (field: keyof FormErrors) => {
  if (formErrors.value[field]) {
    delete formErrors.value[field]
  }
}

/**
 * 验证表单
 */
const validateForm = (): boolean => {
  formErrors.value = {}
  
  if (!uploadForm.value.name.trim()) {
    formErrors.value.name = '请输入视频名称'
  }
  
  if (!uploadForm.value.file) {
    formErrors.value.file = '请选择视频文件'
  }
  
  return Object.keys(formErrors.value).length === 0
}

/**
 * 上传视频
 */
const uploadVideo = async () => {
  if (!validateForm()) return
  
  uploading.value = true
  try {
    await emit('video-upload', {
      name: uploadForm.value.name.trim(),
      annotation: uploadForm.value.annotation.trim(),
      file: uploadForm.value.file!
    })
    
    resetUploadForm()
    
  } catch (error) {
    console.error('视频上传失败:', error)
    // 错误处理可以在这里添加用户提示
  } finally {
    uploading.value = false
  }
}

/**
 * 删除视频
 */
const deleteVideo = async (videoId: number) => {
  if (!confirm('确定要删除这个视频吗？此操作不可撤销。')) return

  deletingId.value = videoId
  try {
    await emit('video-delete', videoId)
  } catch (error) {
    console.error('删除视频失败:', error)
    // 错误处理可以在这里添加用户提示
  } finally {
    deletingId.value = null
  }
}

/**
 * 预览视频
 */
const previewVideo = (video: VideoItem) => {
  previewVideoData.value = video
}

/**
 * 关闭预览
 */
const closePreview = () => {
  previewVideoData.value = null
}

/**
 * 刷新视频列表
 */
const refreshVideos = () => {
  // 这里可以触发父组件重新加载视频列表
  console.log('刷新视频列表')
}

/**
 * 重置上传表单
 */
const resetUploadForm = () => {
  uploadForm.value = {
    name: '',
    annotation: '',
    file: null
  }
  formErrors.value = {}
  dragOver.value = false
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// ========== 工具函数 ==========

/**
 * 格式化文件大小
 */
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 格式化时间
 */
const formatTime = (timeString: string): string => {
  return new Date(timeString).toLocaleString('zh-CN')
}

/**
 * 格式化视频时长
 */
const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.media-management {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

/* 头部样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e8e8e8;
}

.header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.stats {
  display: flex;
  gap: 16px;
  font-size: 0.875rem;
}

.video-count {
  color: #374151;
  font-weight: 500;
}

.total-size {
  color: #6b7280;
}

/* 上传区域样式 */
.upload-section {
  margin-bottom: 32px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.upload-header {
  margin-bottom: 20px;
}

.upload-header h4 {
  margin: 0 0 4px 0;
  color: #374151;
  font-size: 1.125rem;
}

.upload-tip {
  color: #6b7280;
  font-size: 0.875rem;
}

/* 表单样式 */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.required {
  color: #ef4444;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error {
  border-color: #ef4444;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

/* 文件上传区域 */
.file-upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.file-upload-area:hover,
.file-upload-area.drag-over {
  border-color: #3b82f6;
  background: #f0f7ff;
}

.file-upload-area.has-file {
  border-color: #10b981;
  border-style: solid;
}

.file-upload-content {
  pointer-events: none;
}

.upload-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.upload-text {
  font-weight: 500;
  color: #374151;
  margin-bottom: 4px;
}

.upload-hint {
  color: #6b7280;
  font-size: 0.875rem;
}

.file-info {
  text-align: center;
}

.file-name {
  font-weight: 500;
  color: #065f46;
  margin-bottom: 4px;
}

.file-size {
  color: #059669;
  font-size: 0.875rem;
}

.file-input-hidden {
  display: none;
}

/* 错误信息 */
.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 4px;
}

/* 上传按钮 */
.upload-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.upload-btn,
.cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-btn {
  background: #3b82f6;
  color: white;
}

.upload-btn:hover:not(:disabled) {
  background: #2563eb;
}

.upload-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.cancel-btn {
  background: #6b7280;
  color: white;
}

.cancel-btn:hover:not(:disabled) {
  background: #4b5563;
}

/* 加载动画 */
.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 视频列表区域 */
.video-list-section {
  border-top: 1px solid #e8e8e8;
  padding-top: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h4 {
  margin: 0;
  color: #374151;
  font-size: 1.125rem;
}

.refresh-btn {
  padding: 6px 12px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
}

.refresh-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

/* 视频项样式 */
.video-list {
  space-y: 12px;
}

.video-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
  transition: all 0.2s;
  gap: 16px;
}

.video-item:hover {
  background: #f3f4f6;
}

.video-item.deleting {
  opacity: 0.6;
  background: #fef2f2;
}

.video-preview {
  position: relative;
  flex-shrink: 0;
}

.video-icon {
  font-size: 2rem;
}

.video-duration {
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
}

.video-info {
  flex: 1;
  min-width: 0;
}

.video-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
  font-size: 1rem;
}

.video-annotation {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-meta {
  display: flex;
  gap: 16px;
  font-size: 0.75rem;
  color: #9ca3af;
  flex-wrap: wrap;
}

.meta-label {
  font-weight: 500;
}

.video-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.preview-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-btn {
  background: #10b981;
  color: white;
}

.preview-btn:hover {
  background: #059669;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background: #dc2626;
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.deleting-spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 1.125rem;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 0.875rem;
}

/* 加载状态 */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  color: #6b7280;
}

/* 预览模态框 */
.video-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
}

.close-btn:hover {
  color: #374151;
}

.modal-body {
  padding: 20px;
}

.preview-video {
  width: 100%;
  max-height: 60vh;
  border-radius: 8px;
}

.no-preview {
  text-align: center;
  padding: 48px;
  color: #6b7280;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .media-management {
    padding: 16px;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .stats {
    align-self: stretch;
    justify-content: space-between;
  }
  
  .video-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .video-actions {
    align-self: stretch;
    justify-content: flex-end;
  }
  
  .video-meta {
    flex-direction: column;
    gap: 4px;
  }
  
  .upload-actions {
    flex-direction: column;
  }
}
</style>