<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 transition-opacity duration-300" @click.self="$emit('cancel')">
    <div class="bg-white rounded-xl p-6 max-w-3xl w-full mx-4 max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-serif text-amber-700">裁剪头像</h3>
        <button class="text-gray-500 hover:text-gray-700 transition-colors" @click="$emit('cancel')">
          <i class="fa-solid fa-xmark text-xl"></i>
        </button>
      </div>
      
      <div class="cropper-container mb-4">
        <Cropper
          ref="cropper"
          class="cropper"
          :src="imageSrc"
          :stencil-props="{
            aspectRatio: 1,
            movable: true,
            resizable: true,
          }"
          :stencil-component="CircleStencil"
          :resize-image="{
            adjustStencil: false
          }"
          image-restriction="stencil"
        />
      </div>

      <div class="flex justify-between items-center">
        <div class="flex gap-2">
          <button
            @click="rotateLeft"
            class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            title="向左旋转"
          >
            <i class="fa-solid fa-rotate-left"></i>
          </button>
          <button
            @click="rotateRight"
            class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            title="向右旋转"
          >
            <i class="fa-solid fa-rotate-right"></i>
          </button>
          <button
            @click="flipHorizontal"
            class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            title="水平翻转"
          >
            <i class="fa-solid fa-left-right"></i>
          </button>
          <button
            @click="flipVertical"
            class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            title="垂直翻转"
          >
            <i class="fa-solid fa-up-down"></i>
          </button>
        </div>
        <div class="flex gap-3">
          <button
            class="px-4 py-2 border border-amber-300 text-amber-700 rounded-lg hover:bg-amber-50 transition-colors"
            @click="$emit('cancel')"
            :disabled="loading"
          >
            取消
          </button>
          <button
            class="px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            @click="confirmCrop"
            :disabled="loading"
          >
            <span v-if="loading">
              <i class="fa-solid fa-spinner fa-spin mr-2"></i>处理中...
            </span>
            <span v-else>确认使用</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const props = defineProps<{
  imageSrc: string
}>()

const emit = defineEmits(['confirm', 'cancel'])

const cropper = ref()
const loading = ref(false)

const confirmCrop = () => {
  if (!cropper.value) return
  loading.value = true
  
  const { canvas } = cropper.value.getResult()
  if (canvas) {
    canvas.toBlob((blob: Blob | null) => {
      if (blob) {
        const reader = new FileReader()
        reader.onloadend = () => {
          emit('confirm', reader.result as string)
          loading.value = false
        }
        reader.readAsDataURL(blob)
      } else {
        loading.value = false
      }
    }, 'image/png')
  } else {
    loading.value = false
  }
}

const rotateLeft = () => {
  cropper.value?.rotate(-90)
}

const rotateRight = () => {
  cropper.value?.rotate(90)
}

const flipHorizontal = () => {
  cropper.value?.flip(true, false)
}

const flipVertical = () => {
  cropper.value?.flip(false, true)
}
</script>

<style scoped>
.cropper-container {
  width: 100%;
  height: 500px;
  background: #f3f4f6;
  border-radius: 0.5rem;
  overflow: hidden;
}

.cropper {
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(45deg, #e5e7eb 25%, transparent 25%),
    linear-gradient(-45deg, #e5e7eb 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #e5e7eb 75%),
    linear-gradient(-45deg, transparent 75%, #e5e7eb 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

:deep(.vue-advanced-cropper__background),
:deep(.vue-advanced-cropper__foreground) {
  background: transparent;
}

:deep(.vue-line) {
  border-color: #f59e0b;
}

:deep(.vue-handler) {
  background: #f59e0b;
  border-color: #d97706;
}

:deep(.vue-simple-line) {
  border-color: #f59e0b;
}
</style>
