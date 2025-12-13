<template>
  <div class="splash-screen" :class="{ 'splash-hidden': !visible }">
    <div class="splash-image"></div>
    <div class="splash-content">
      <div class="splash-logo">{{ title }}</div>
      <div class="splash-tagline">运动数据管理系统</div>
      <div class="splash-progress-container">
        <div class="splash-progress">
          <div class="progress-bar"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const title = import.meta.env.VITE_TITLE ;

interface Props {
  duration?: number;
}

const props = withDefaults(defineProps<Props>(), {
  duration: 3000
});

const visible = ref(true);

onMounted(() => {
  setTimeout(() => {
    visible.value = false;
  }, props.duration);
});
</script>

<style scoped>
/* 保持原有的CSS样式，这里省略以节省空间 */
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  transition: opacity 0.8s ease-out;
  background-color: #f0f7ee;
  overflow: hidden;
}

.splash-hidden {
  opacity: 0;
  pointer-events: none;
}

.splash-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/login_bg_0.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.9;
  filter: brightness(0.9);
  z-index: 1;
}

.splash-content {
  position: relative;
  z-index: 2;
  text-align: center;
  width: 90%;
}

.splash-logo {
  font-family: 'Bubblegum Sans', cursive;
  font-size: 8rem;
  color: #ffffff;
  text-shadow:
    3px 3px 0px #2e7d32,
    5px 5px 10px rgba(0,0,0,0.3);
  margin-bottom: 20px;
  transform: translateY(30px);
  opacity: 0;
  animation: logoRise 1.5s ease-out forwards;
  line-height: 1.2;
}

.splash-tagline {
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: 500;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
  margin-bottom: 30px;
  opacity: 0;
  animation: fadeIn 1s ease-out 0.5s forwards;
}

.splash-progress-container {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 50px;
}

.splash-progress {
  width: 300px;
  height: 4px;
  background: rgba(255,255,255,0.3);
  border-radius: 3px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #ffffff, #e8f5e9);
  width: 0%;
  animation: progressFill 2s linear forwards;
}

@keyframes logoRise {
  0% { transform: translateY(30px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes progressFill {
  from { width: 0%; }
  to { width: 100%; }
}

@media (max-width: 768px) {
  .splash-logo {
    font-size: 6rem;
  }
}

@media (max-width: 576px) {
  .splash-logo {
    font-size: 4rem;
  }

  .splash-tagline {
    font-size: 1.5rem;
  }

  .splash-progress {
    width: 200px;
  }
}
</style>
