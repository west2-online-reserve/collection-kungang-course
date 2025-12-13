<template>
  <div class="min-h-screen bg-amber-50/30 p-8 pt-20 flex items-center justify-center">
    <div class="max-w-2xl w-full text-center">
      <h1 class="text-5xl font-serif text-amber-900 mb-8 animate-fade-in-up">旅程结束</h1>
      <div class="bg-white/60 backdrop-blur-sm rounded-xl p-12 shadow-lg border border-amber-100 animate-fade-in-up animation-delay-200">
        <p class="text-xl text-gray-700 leading-relaxed mb-8">
          恭喜你完成了福州大学校史之旅！
        </p>
        <button @click="$router.push('/home')" class="px-8 py-3 bg-amber-700 text-white rounded-full hover:bg-amber-800 transition-colors shadow-md">
          返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
