<template>
  <div class="row mb-2">
    <div class="col-12">
      <h2 class="text-success fw-bold">欢迎回来，{{ userName }}！</h2>
      <p class="text-muted">{{ currentDate }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

defineProps<{
  userName?: string;
}>();

const getBeijingDate = () => {
  const now = new Date()
  // 调整为北京时间 (UTC+8)
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000)
  return beijingTime.toISOString().split('T')[0]
}
const currentDate = computed(() => {
  return getBeijingDate();
});
</script>
