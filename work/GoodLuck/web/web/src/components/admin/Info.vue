<template>
  <div class="stats-cards">
    <div 
      v-for="(card, index) in cardsData" 
      :key="index" 
      class="stat-card"
      :class="`card-${index + 1}`"
    >
      <div class="card-icon">
        <component :is="card.icon" />
      </div>
      <div class="card-content">
        <div class="card-title">{{ card.title }}</div>
        <div class="card-value">{{ card.value }}</div>
        <!-- <div class="card-info" :class="card.trendClass">
          <span v-if="card.trendIcon" class="trend-icon">{{ card.trendIcon }}</span>
          {{ card.info }}
        </div> -->
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

//定义Props接口，用于接收附件传来的数据
interface Props {
  data?: {
    loginCount: number
    onlineUsers: number
    pendingFeedback: number
    mediaFiles: number
  }
}

const props = withDefaults(defineProps<Props>(), {
  data: () => ({
    loginCount: 0,
    onlineUsers: 0,
    pendingFeedback: 0,
    mediaFiles: 0
  })
})

// 图标组件（简单实现，实际项目中可以使用图标库）
const LoginIcon = { template: '<div class="icon-login">👤</div>' }
const UserIcon = { template: '<div class="icon-user">👥</div>' }
const AlertIcon = { template: '<div class="icon-alert">⚠️</div>' }
const MediaIcon = { template: '<div class="icon-media">📁</div>' }

// 卡片数据接口
interface CardData {
  type: string
  title: string
  value: number
  displayValue: string
  info: string
  trendIcon?: string
  trendClass?: string
  icon: any
}

// 响应式数据
const cardsData = computed<CardData[]>(() => [
  {
    type: 'login',
    title: '今日登录量',
    value: props.data.loginCount,
    displayValue: new Intl.NumberFormat().format(props.data.loginCount),
    info: '12.5% 相比昨日',
    trendIcon: '↗',
    trendClass: 'trend-up',
    icon: LoginIcon
  },
  {
    type: 'online',
    title: '当前注册用户',
    value: props.data.onlineUsers,
    displayValue: new Intl.NumberFormat().format(props.data.onlineUsers),
    info: '峰值时段 16:00',
    icon: UserIcon
  },
  {
    type: 'feedback',
    title: '待处理反馈',
    value: props.data.pendingFeedback,
    displayValue: new Intl.NumberFormat().format(props.data.pendingFeedback),
    info: '2个未读需紧急处理', 
    trendClass: 'trend-alert',
    icon: AlertIcon
  },
  {
    type: 'media',
    title: '媒体文件数',
    value: props.data.mediaFiles,
    displayValue: new Intl.NumberFormat().format(props.data.mediaFiles),
    info: '3个新视频待发布',
    icon: MediaIcon
  }
])

// 如果需要，可以添加计算属性或方法
// 例如：格式化数值、处理趋势等
</script>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  padding: 20px;
  background-color: #f8f9fa;
}

.stat-card {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 20px;
}

.card-1 .card-icon {
  background-color: #e6f7ff;
  color: #1890ff;
}

.card-2 .card-icon {
  background-color: #f6ffed;
  color: #52c41a;
}

.card-3 .card-icon {
  background-color: #fff2e8;
  color: #fa8c16;
}

.card-4 .card-icon {
  background-color: #f9f0ff;
  color: #722ed1;
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.card-value {
  font-size: 28px;
  font-weight: 600;
  color: #1f1f1f;
  margin-bottom: 6px;
}

.card-info {
  font-size: 13px;
  display: flex;
  align-items: center;
}

.trend-icon {
  margin-right: 4px;
}

.trend-up {
  color: #52c41a;
}

.trend-alert {
  color: #ff4d4f;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .card-value {
    font-size: 24px;
  }
}
</style>