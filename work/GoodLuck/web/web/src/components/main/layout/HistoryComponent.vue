<template>
  <div class="history-wrapper">
    <!-- 左侧主内容 -->
    <div class="history">
      <h2 class="page-title">历史记录查询</h2>

      <!-- 查询条件区域 -->
      <div class="search-section">
        <!-- <div class="search-item">
          <label>时间范围</label>
          <select v-model="searchForm.timeRange">
            <option value="本月">本月</option>
            <option value="本周">本周</option>
            <option value="近三月">近三月</option>
          </select>
        </div> -->

        <div class="search-item">
          <label>搜索关键词</label>
          <input type="text" v-model="searchForm.keyword" placeholder="搜索记录..." />
        </div>
      </div>

      <!-- 表格区域 -->
      <div class="table-section">
        <table class="history-table">
          <thead>
            <tr>
              <th>历史记录</th>
              <th>时间/时间</th>
              <th>评分</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in paginatedList" :key="index">
              <td>
                <span class="index-badge">{{ (currentPage - 1) * pageSize + index + 1 }}</span>
                {{ item.project }}
              </td>
              <td>{{ item.time }}</td>
              <td>
                <span class="score-tag" :class="getScoreClass(item.score)">{{ item.score }}</span>
              </td>
              <td>
                <a href="javascript:;" class="action-link" @click="openDetailModal(item)"
                  >查看详情</a
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-if="paginatedList.length === 0">
        <div class="empty-icon">📄</div>
        <p class="empty-title">暂无历史记录</p>
        <p class="empty-desc">开始新的测试后将在此处显示您的历史记录</p>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
          下一页
        </button>
      </div>
    </div>

    <!-- 右侧日历 -->
    <div class="calendar-widget">
      <div class="calendar-header">
        <button class="nav-btn" @click="prevMonth">&lt;</button>
        <span class="month-title">{{ currentYear }}年{{ currentMonth + 1 }}月</span>
        <button class="nav-btn" @click="nextMonth">&gt;</button>
      </div>
      <div class="calendar-weekdays">
        <span v-for="day in weekDays" :key="day">{{ day }}</span>
      </div>
      <div class="calendar-days">
        <span
          v-for="(day, index) in calendarDays"
          :key="index"
          class="day-cell"
          :class="{
            'other-month': !day.currentMonth,
            trained: day.trained,
            today: day.isToday,
          }"
        >
          {{ day.date }}
        </span>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div class="modal-overlay" v-if="showModal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeModal">✕</button>

        <h2 class="modal-title">{{ currentDetail.project }}</h2>

        <div class="modal-info-row">
          <span class="modal-label">测试时间：</span>
          <span class="modal-value">{{ currentDetail.time }}</span>
        </div>

        <div class="modal-info-row">
          <span class="modal-label">评分：</span>
          <span class="modal-score" :class="getScoreClass(currentDetail.score)">
            {{ currentDetail.score }}
          </span>
        </div>

        <div class="modal-evaluation">
          <h3 class="modal-section-title">评价与改进措施</h3>
          <div class="modal-evaluation-content">
            {{ currentDetail.evaluation }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import './styles/History.css'

import { ref, reactive, computed, onMounted, watch } from 'vue'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''


// 获取token的函数（后续根据你的认证方式修改）
const getToken = () => {
  return localStorage.getItem('token') || ''
}

interface HistoryItem {
  id?: number
  project: string
  time: string
  date: Date
  score: number
}



const searchForm = reactive({
  timeRange: '近三月',
  keyword: '',
})

const loading = ref(false)
const trainedDatesFromServer = ref<string[]>([])

// 日历相关
const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth())

// ============ API 调用函数 ============

// 获取历史记录列表
const fetchHistoryList = async () => {
  const token = getToken()
  if (!token) return

  loading.value = true
  try {


    const response = await fetch(`${API_BASE_URL}/api/history`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('获取历史记录失败')

    const data = await response.json()
    // console.log('历史记录数据:', data)
    rawHistoryList.value = data.data.data.map((item: HistoryItem) => ({
      id: item.id,
      project: item.project,
      time: item.time,
      date: new Date(item.date),
      score: item.score,
    }))
  } catch (error) {
    console.error('获取历史记录失败:', error)
  } finally {
    loading.value = false
  }
}


// 获取单条历史记录详情（从服务器）
const fetchHistoryDetailFromServer = async (id: number) => {
  const token = getToken()
  if (!token) return null

  try {
    const response = await fetch(`${API_BASE_URL}/api/history/detail/${id}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('获取历史详情失败')

    const data = await response.json()
    // 期望返回格式: { code: 200, message: 'success', data: { project, time, score, evaluation } }
    return data.data
  } catch (error) {
    console.error('获取历史详情失败:', error)
    return null
  }
}

// ============ 生命周期和监听 ============

// 组件挂载时加载数据
onMounted(() => {
  // 如果需要从服务器加载，取消下面注释
  fetchHistoryList()


})




// ============ 计算属性 ============

// 训练过的日期
const trainedDates = computed(() => {
  // 优先使用服务器数据
  if (trainedDatesFromServer.value.length > 0) {
    return trainedDatesFromServer.value.map((dateStr) => {
      const d = new Date(dateStr)
      return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`
    })
  }
  // 否则从本地历史记录提取
  return rawHistoryList.value.map((item) => {
    const d = item.date
    return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`
  })
})

// 生成日历天数
const calendarDays = computed(() => {
  const days: { date: number; currentMonth: boolean; trained: boolean; isToday: boolean }[] = []
  const year = currentYear.value
  const month = currentMonth.value

  // 当月第一天是星期几
  const firstDay = new Date(year, month, 1).getDay()
  // 当月天数
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  // 上月天数
  const daysInPrevMonth = new Date(year, month, 0).getDate()

  const today = new Date()
  const todayStr = `${today.getFullYear()}-${today.getMonth()}-${today.getDate()}`

  // 上月的日期
  for (let i = firstDay - 1; i >= 0; i--) {
    const date = daysInPrevMonth - i
    const dateStr = `${year}-${month - 1}-${date}`
    days.push({
      date,
      currentMonth: false,
      trained: trainedDates.value.includes(dateStr),
      isToday: false,
    })
  }

  // 当月的日期
  for (let i = 1; i <= daysInMonth; i++) {
    const dateStr = `${year}-${month}-${i}`
    days.push({
      date: i,
      currentMonth: true,
      trained: trainedDates.value.includes(dateStr),
      isToday: dateStr === todayStr,
    })
  }

  // 下月的日期（补齐到42天）
  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    const dateStr = `${year}-${month + 1}-${i}`
    days.push({
      date: i,
      currentMonth: false,
      trained: trainedDates.value.includes(dateStr),
      isToday: false,
    })
  }

  return days
})

const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

// 分页相关
const currentPage = ref(1)
const pageSize = 10
// 原始数据列表（本地模拟数据，后续可删除）
const rawHistoryList = ref<HistoryItem[]>([
  // {
    // id: 1,
    // project: '引体向上8个',
    // time: '2025-11-28 09:24',
    // date: new Date('2025-11-28'),
    // score: 78,
  // },

])

// 计算过滤后的列表
const historyList = computed(() => {
  return rawHistoryList.value.filter((item) => {
    // 时间范围过滤

    let startDate: Date
    switch (searchForm.timeRange) {

      default:
        startDate = new Date(0)
    }
    if (item.date < startDate) return false

    // 关键词过滤
    if (searchForm.keyword && !item.project.includes(searchForm.keyword)) return false

    return true
  })
})

// 总页数
const totalPages = computed(() => Math.ceil(historyList.value.length / pageSize))

// 当前页数据
const paginatedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return historyList.value.slice(start, start + pageSize)
})

// 搜索条件变化时重置页码
watch([() => searchForm.timeRange, () => searchForm.keyword], () => {
  currentPage.value = 1
  // 如果需要从服务器加载，取消下面注释
  // fetchHistoryList({ timeRange: searchForm.timeRange, keyword: searchForm.keyword })
})

// 根据分数返回样式类
const getScoreClass = (score: number) => {
  if (score >= 90) return 'score-excellent'
  if (score >= 70) return 'score-good'
  return 'score-normal'
}

// 弹窗相关
const showModal = ref(false)
const currentDetail = ref({
  project: '',
  time: '',
  score: 0,
  evaluation: '',
})

// 模拟详情数据
const detailData: Record<string, string> = {

}

const openDetailModal = async (item: HistoryItem) => {
  // 先显示弹窗，使用本地数据
  currentDetail.value = {
    project: item.project,
    time: item.time,
    score: item.score,
    evaluation: detailData[item.project] || '加载中...',
  }
  showModal.value = true

  // 如果有 id，尝试从服务器获取详细数据
  if (item.id) {
    const serverDetail = await fetchHistoryDetailFromServer(item.id)
    if (serverDetail) {
      currentDetail.value = {
        project: serverDetail.project || item.project,
        time: serverDetail.time || item.time,
        score: serverDetail.score || item.score,
        evaluation: serverDetail.evaluation || detailData[item.project] || '暂无评价信息',
      }
    } else {
      // 服务器获取失败，使用本地模拟数据
      currentDetail.value.evaluation = detailData[item.project] || '暂无评价信息'
    }
  }
}

const closeModal = () => {
  showModal.value = false
}
</script>

<style scoped>

</style>
