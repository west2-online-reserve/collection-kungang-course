<template>
  <div class="login-chart-container">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>图表加载中...</span>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <span>{{ error }}</span>
      <button @click="initChart" class="retry-btn">重试</button>
    </div>
    
    <!-- 空数据状态 -->
    <div v-else-if="!hasValidData" class="empty-state">
      <span>暂无数据</span>
    </div>
    
    <!-- 正常显示 -->
    <div v-else>
      <div class="chart-header">
        <div class="chart-title">用户登录流量分析</div>
        <div class="time-filters">
          <div 
           class="time-filter active"
          >7天</div>
         
        </div>
      </div>
      
      <div class="date-range">{{ chartData.dateRange }}</div>
      
      <div class="chart-wrapper">
        <canvas ref="chartCanvas"></canvas>
      </div>
      
      <div class="chart-legend">
        <div class="legend-item">
          <div class="legend-color legend-login"></div>
          <span>登录量 {{ chartData.totalLogin.toLocaleString() }}</span>
        </div>
        <div class="legend-item">
          <div class="legend-color legend-active"></div>
          <span>活跃用户 {{ chartData.totalActive.toLocaleString() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { Chart, type ChartConfiguration, type ChartData, type ChartOptions } from 'chart.js/auto'

// 定义Props接口
interface Props {
  chartData: {
    loginData: number[]
    activeData: number[]
    dates: string[]
    dateRange: string
    totalLogin: number
    totalActive: number
  }
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  chartData: () => ({
    loginData: [],
    activeData: [],
    dates: [],
    dateRange: '',
    totalLogin: 0,
    totalActive: 0
  })
})

const chartCanvas = ref<HTMLCanvasElement | null>(null)
const chartInstance = ref<Chart | null>(null)
const error = ref<string | null>(null)
const isMounted = ref(false)

// 计算属性：检查数据是否有效
const hasValidData = computed(() => {
  return props.chartData && 
         Array.isArray(props.chartData.loginData) && 
         props.chartData.loginData.length > 0 &&
         Array.isArray(props.chartData.dates) && 
         props.chartData.dates.length > 0
})

// 计算Y轴最大值
const getYAxisMax = computed(() => {
  if (!hasValidData.value) return 15000
  
  const allData = [...props.chartData.loginData, ...props.chartData.activeData]
  const maxValue = Math.max(...allData)
  // 向上取整到最近的3000的倍数
  return Math.ceil(maxValue / 3000) * 3000 || 15000
})

// 初始化图表
const initChart = () => {
  try {
    if (!chartCanvas.value || !hasValidData.value) {
      console.warn('图表数据未准备好，等待数据加载...')
      return
    }
    
    const ctx = chartCanvas.value.getContext('2d')
    if (!ctx) {
      throw new Error('无法获取Canvas上下文')
    }
    
    // 销毁之前的图表实例
    if (chartInstance.value) {
      chartInstance.value.destroy()
    }
    
    console.log('初始化图表，数据:', props.chartData)
    
    // 使用正确的 Chart.js 配置类型
    const config: ChartConfiguration<'line'> = {
      type: 'line',
      data: {
        labels: props.chartData.dates,
        datasets: [
          {
            label: '登录量',
            data: props.chartData.loginData,
            borderColor: '#1890ff',
            backgroundColor: 'rgba(24, 144, 255, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: '#1890ff',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            fill: true
          },
          {
            label: '活跃用户',
            data: props.chartData.activeData,
            borderColor: '#52c41a',
            backgroundColor: 'rgba(82, 196, 26, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: '#52c41a',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.3,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#e1e5e9',
            borderWidth: 1,
            cornerRadius: 6,
            displayColors: true,
            callbacks: {
              label: function(context) {
                if (context.parsed.y === null || context.parsed.y === undefined) {
                  return ''
                }
                const value = context.parsed.y.toLocaleString()
                return `${context.dataset.label}: ${value}`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            suggestedMax: getYAxisMax.value,
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            },
            border: {
              display: false
            },
            ticks: {
              callback: function(value) {
                return typeof value === 'number' ? value.toLocaleString() : ''
              },
              color: '#666666',
              font: {
                size: 12,
                family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
              },
              stepSize: 3000,
            },
            title: {
              display: true,
              text: '流量',
              color: '#666666',
              font: {
                size: 12,
                weight: 'normal'
              },
              padding: { top: 0, bottom: 10 }
            }
          },
          x: {
            grid: {
              display: false
            }, 
            border: {
              display: false
            },
            ticks: {
              color: '#666666',
              font: {
                size: 12,
                family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
              }
            }
          }
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false
        },
        elements: {
          line: {
            tension: 0.3
          },
          point: {
            hoverBackgroundColor: '#ffffff',
            hoverBorderColor: '#ffffff',
            hoverBorderWidth: 3
          }
        }
      }
    }
    
    chartInstance.value = new Chart(ctx, config)
    
    error.value = null
    console.log('图表初始化成功')
    
  } catch (err) {
    error.value = '图表初始化失败: ' + (err instanceof Error ? err.message : '未知错误')
    console.error('图表初始化失败:', err)
  }
}

// 更新图表数据
const updateChartData = () => {
  if (!chartInstance.value || !hasValidData.value) return
  
  // 安全地更新数据
  const chartData = chartInstance.value.data
  if (chartData) {
    chartData.labels = props.chartData.dates
    if (chartData.datasets && chartData.datasets.length >= 2) {
      // 使用类型断言确保类型安全
      const datasets = chartData.datasets as any[]
      datasets[0].data = [...props.chartData.loginData]
      datasets[1].data = [...props.chartData.activeData]
    }
  }
  
  // 更新Y轴最大值 - 使用 suggestedMax
  if (chartInstance.value.options.scales?.y) {
    const yScale = chartInstance.value.options.scales.y as any
    yScale.suggestedMax = getYAxisMax.value
  }
  
  chartInstance.value.update()
}


// 监听props变化
watch(() => props.chartData, (newData) => {
  console.log('图表数据更新:', newData)
  if (isMounted.value && hasValidData.value) {
    nextTick(() => {
      if (chartInstance.value) {
        updateChartData()
      } else {
        initChart()
      }
    })
  }
}, { deep: true })

// 监听loading状态
watch(() => props.loading, (isLoading) => {
  console.log('Loading状态变化:', isLoading)
  if (!isLoading && hasValidData.value && isMounted.value) {
    nextTick(() => {
      if (!chartInstance.value) {
        initChart()
      }
    })
  }
})

onMounted(() => {
  console.log('图表组件挂载')
  isMounted.value = true
  
  // 等待数据准备好后初始化图表
  if (!props.loading && hasValidData.value) {
    nextTick(initChart)
  }
})

onUnmounted(() => {
  isMounted.value = false
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
})
</script>

<style scoped>
.login-chart-container {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin: 20px 0;
  transition: all 0.3s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  min-height: 400px;
}

.login-chart-container:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

/* 简化时间筛选器样式，因为现在只有一个选项 */
.time-filters {
  display: flex;
  background: #f0f2f5;
  border-radius: 6px;
  padding: 4px;
}

.time-filter {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  color: #1890ff;
  font-weight: 500;
  cursor: default; /* 移除可点击效果 */
}

/* 移除hover效果，因为现在不可点击 */
.time-filter:hover {
  background: white; /* 保持白色背景 */
}

.date-range {
  font-size: 13px;
  color: #666;
  margin-bottom: 20px;
  text-align: center;
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}

.chart-legend {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 30px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #666;
}

.legend-color {
  width: 20px;
  height: 3px;
  margin-right: 8px;
  border-radius: 2px;
}

.legend-login {
  background-color: #1890ff;
}

.legend-active {
  background-color: #52c41a;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #666;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-btn {
  margin-top: 10px;
  padding: 6px 12px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background: #40a9ff;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .time-filters {
    width: 100%;
    justify-content: center;
  }
  
  .login-chart-container {
    padding: 16px;
  }
  
  .chart-wrapper {
    height: 250px;
  }
}
</style>