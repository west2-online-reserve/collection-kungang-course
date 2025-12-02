<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 p-8 pt-20">
    <div class="max-w-7xl mx-auto">
      <!-- 标题区 -->
      <div class="mb-12 text-center">
        <h1 class="text-5xl font-serif font-bold text-amber-900 mb-4">
          <i class="fa-solid fa-graduation-cap mr-3"></i>学院介绍
        </h1>
        <p class="text-xl text-gray-600">了解各个学院的风采与特色</p>
      </div>
      
      <!-- 学院卡片网格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(college, index) in colleges"
          :key="college.id"
          :style="{ animationDelay: `${index * 0.1}s` }"
          class="animate-fade-in-up">
          <CollegeCard :college="college" />
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-if="colleges.length === 0" class="text-center py-20">
        <i class="fa-solid fa-inbox text-6xl text-gray-300 mb-4"></i>
        <p class="text-gray-500">暂无学院信息</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CollegeCard from '@/components/college/CollegeCard.vue'
import collegesData from '@/components/college/colleges-data.json'

const colleges = ref(collegesData)

onMounted(() => {
  // 可以在这里添加加载动画等
})
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
  opacity: 0;
}
</style>
