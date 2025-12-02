<script setup lang="ts"></script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="page-fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.page-fade-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.page-fade-leave-to {
  opacity: 0;
  transform: scale(1.05);
}

/* =========================
   内容区淡入效果（避免影响 fixed 元素）
   ========================= */

.page-fade-enter-active .page-content * {
  animation: fadeInUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
  opacity: 0;
  transform: translateY(20px);
}

/* 分层延迟 */
.page-fade-enter-active .page-content h1,
.page-fade-enter-active .page-content h2,
.page-fade-enter-active .page-content h3 {
  animation-delay: 0.2s;
}

.page-fade-enter-active .page-content p,
.page-fade-enter-active .page-content span,
.page-fade-enter-active .page-content label {
  animation-delay: 0.3s;
}

.page-fade-enter-active .page-content input,
.page-fade-enter-active .page-content button,
.page-fade-enter-active .page-content select,
.page-fade-enter-active .page-content textarea {
  animation-delay: 0.4s;
}

.page-fade-enter-active .page-content img,
.page-fade-enter-active .page-content .img-container {
  animation-delay: 0.5s;
}

.page-fade-enter-active .page-content .secondary-content {
  animation-delay: 0.6s;
}

.page-fade-enter-active .page-content .tertiary-content {
  animation-delay: 0.7s;
}

/* 动画关键帧 */
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

