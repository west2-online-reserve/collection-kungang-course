
<template>
  <Suspense>
    <template #default>
      <router-view v-slot="{ Component, route }">
    <keep-alive :include="['Main']" :max="5">
      <component :is="Component" :key="route.name" />
    </keep-alive>
  </router-view>
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>
<script setup lang="ts">

// 这里可以放一些全局的初始化逻辑
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>