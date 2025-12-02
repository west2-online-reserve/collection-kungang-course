<template>
  <div class="h-screen bg-parchment relative">
    <!-- 背景图 (可选，如果所有页面都共用) -->
    <div
      class="fixed inset-0 bg-[url('https://images.unsplash.com/photo-1529590003495-2e0a378906d1?q=80&w=1920&auto=format&fit=crop')] bg-center bg-cover opacity-10 -z-10"
    ></div>

    <TopBar />
    <Sidebar />

    <!-- 页面内容 -->
    <div
      class="relative z-0 h-screen overflow-y-auto transition-all duration-300"
      :style="{
        paddingLeft: ui.navExpanded ? '12rem' : '3rem',
      }"
    >
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue'
import TopBar from '@/components/TopBar.vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
