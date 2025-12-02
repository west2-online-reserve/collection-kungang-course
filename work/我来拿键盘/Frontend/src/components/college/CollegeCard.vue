<template>
  <div
    @click="$router.push(`/college/${college.id}`)"
    class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer transform hover:-translate-y-2 border-2 border-amber-100 max-w-xl w-full mx-auto">
    <!-- 封面图片 -->
    <div class="relative h-48 overflow-hidden">
      <img :src="college.cover" :alt="college.name" class="w-full h-full object-cover transition-transform duration-300 hover:scale-110" />
      <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-transparent to-black/50"></div>
      <div class="absolute bottom-4 left-4 text-white">
        <h3 class="text-2xl font-bold font-serif">{{ college.name }}</h3>
        <p class="text-sm text-amber-200">{{ college.shortName }}</p>
      </div>
    </div>

    <!-- 描述 -->
    <div class="p-6">
      <p class="text-gray-600 line-clamp-2 mb-4">{{ college.description }}</p>

      <!-- 统计信息 -->
      <div class="flex items-center justify-between text-sm text-gray-500">
        <div class="flex items-center gap-1">
          <i class="fa-solid fa-chalkboard-user text-amber-600"></i>
          <span>{{ college.teachers.length }} 位教师</span>
        </div>
        <div class="flex items-center gap-1">
          <i class="fa-solid fa-flask text-amber-600"></i>
          <span>{{ college.labs.length }} 个实验室</span>
        </div>
      </div>

      <!-- 查看详情按钮 -->
      <div class="mt-4 text-center">
        <span class="inline-block px-4 py-2 bg-amber-700 text-white rounded-lg hover:bg-amber-800 transition-colors">
          查看详情 <i class="fa-solid fa-arrow-right ml-2"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Teacher {
  name: string
  title: string
  research: string
  photo: string
  achievements: string
}

interface Lab {
  name: string
  description: string
  image: string
  equipment: string
}

interface College {
  id: number
  name: string
  shortName: string
  cover: string
  description: string
  introduction: string
  teachers: Teacher[]
  labs: Lab[]
}

defineProps<{
  college: College
}>()
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
