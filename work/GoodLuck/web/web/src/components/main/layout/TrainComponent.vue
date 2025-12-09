<template>
  <div class="train-wrapper">
    <!-- 左侧：训练数据统计 -->
    <div class="train-stats">
      <div class="stats-header">
        <h2 class="stats-title">训练数据统计</h2>
        <button class="help-btn" @click="showHelpModal = true">?</button>
      </div>

      <!-- 图表区域 -->
      <div class="chart-section">
        <div class="chart-header">
          <div class="chart-tabs">
            <button
              class="tab-btn"
              :class="{ active: activeTab === '练习次数趋势' }"
              @click="activeTab = '练习次数趋势'"
            >
              引体向上练习次数趋势
            </button>
          </div>
          <div class="week-nav">
            <button class="week-btn" @click="prevWeek">← 上周</button>
            <span class="week-label">{{ currentWeekLabel }}</span>
            <button class="week-btn" @click="nextWeek" :disabled="isCurrentWeek">下周 →</button>
          </div>
        </div>

        <div class="chart-container">
          <div v-if="weekData.length === 0" class="chart-placeholder">
            <div class="chart-icon">📊</div>
            <p class="chart-text">本周暂无训练数据</p>
          </div>
          <div v-else class="line-chart">
            <div class="chart-y-axis">
              <span v-for="tick in yAxisTicks" :key="tick" class="y-tick">{{ tick }}</span>
            </div>
            <div class="chart-content">
              <svg class="chart-svg" :viewBox="`0 0 ${chartWidth} ${chartHeight}`">
                <!-- 网格线 -->
                <line
                  v-for="tick in yAxisTicks"
                  :key="`grid-${tick}`"
                  :x1="0"
                  :y1="getYPosition(tick)"
                  :x2="chartWidth"
                  :y2="getYPosition(tick)"
                  class="grid-line"
                />

                <!-- 折线 -->
                <polyline :points="linePoints" class="chart-line" />

                <!-- 数据点 -->
                <circle
                  v-for="(point, index) in weekData"
                  :key="index"
                  :cx="getXPosition(index)"
                  :cy="getYPosition(point.count)"
                  r="4"
                  class="chart-point"
                />

                <!-- 数据标签 -->
                <text
                  v-for="(point, index) in weekData"
                  :key="`label-${index}`"
                  :x="getXPosition(index)"
                  :y="getYPosition(point.count) - 10"
                  class="chart-label"
                >
                  {{ point.count }}
                </text>
              </svg>

              <!-- X轴标签 -->
              <div class="chart-x-axis">
                <span v-for="(point, index) in weekData" :key="index" class="x-label">
                  {{ point.label }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 日期计划设置 -->
      <div class="plan-setting-section">
        <h3 class="section-title">设置训练计划</h3>
        <div class="plan-form">
          <div class="form-row">
            <label class="form-label">选择日期</label>
            <input type="date" v-model="planForm.date" class="form-input" />
          </div>

          <div class="form-row">
            <label class="form-label">训练项目</label>
            <input
              type="text"
              v-model="planForm.project"
              placeholder="例如：引体向上、俯卧撑等"
              class="form-input"
            />
          </div>

          <div class="form-row">
            <label class="form-label">目标数量</label>
            <input
              type="number"
              v-model="planForm.target"
              placeholder="例如：10"
              class="form-input"
            />
          </div>

          <div class="form-row">
            <label class="form-label">备注说明</label>
            <textarea
              v-model="planForm.note"
              placeholder="可选，添加训练说明或注意事项"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>

          <div class="form-actions">
            <button class="btn-cancel" @click="resetForm">重置</button>
            <button class="btn-submit" @click="submitPlan">创建计划</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧：训练计划统计 -->
    <div class="plan-stats">
      <h2 class="plan-title">训练计划统计</h2>

      <!-- 统计卡片 -->
      <div class="stats-cards">
        <div class="stat-card">
          <div class="card-label">训练计划数量</div>
          <div class="card-value">{{ totalPlans }}</div>
        </div>
        <div class="stat-card">
          <div class="card-label">已完成计划数量</div>
          <div class="card-value">{{ completedPlans }}</div>
        </div>
        <div class="stat-card">
          <div class="card-label">计划完成率</div>
          <div class="card-value">{{ completionRate }}%</div>
        </div>
      </div>

      <!-- 月度训练计划统计 -->
      <div class="monthly-stats">
        <h3 class="section-title">月度训练计划统计</h3>
        <div class="month-tabs">
          <button
            class="month-tab"
            :class="{ active: timeRange === 'week' }"
            @click="timeRange = 'week'"
          >
            本周
          </button>
          <button
            class="month-tab"
            :class="{ active: timeRange === 'month' }"
            @click="timeRange = 'month'"
          >
            本月
          </button>
          <button
            class="month-tab"
            :class="{ active: timeRange === 'threeMonths' }"
            @click="timeRange = 'threeMonths'"
          >
            近三月
          </button>
          <button
            class="month-tab"
            :class="{ active: timeRange === 'halfYear' }"
            @click="timeRange = 'halfYear'"
          >
            半年内
          </button>
          <button
            class="month-tab"
            :class="{ active: timeRange === 'all' }"
            @click="timeRange = 'all'"
          >
            全部时间
          </button>
        </div>
        <div v-if="filteredPlans.length === 0" class="monthly-empty">
          <div class="empty-icon">📅</div>
          <p class="empty-text">暂无月度数据</p>
        </div>
        <div v-else class="monthly-data">
          <div class="data-summary">
            <div class="summary-item">
              <span class="summary-label">计划总数</span>
              <span class="summary-value">{{ filteredPlans.length }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">已完成</span>
              <span class="summary-value completed">{{ filteredCompletedCount }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">未完成</span>
              <span class="summary-value pending">{{
                filteredPlans.length - filteredCompletedCount
              }}</span>
            </div>
          </div>
          <div class="data-list">
            <div v-for="(plan, index) in filteredPlans" :key="index" class="data-item">
              <span class="item-date">{{ plan.date }}</span>
              <span class="item-project">{{ plan.project }}</span>
              <span class="item-status" :class="{ completed: plan.completed }">
                {{ plan.completed ? '✓' : '○' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 本周训练计划 -->
      <div class="weekly-plan">
        <h3 class="section-title">本周训练计划</h3>
        <div v-if="weeklyPlans.length === 0" class="weekly-empty">
          <div class="empty-icon">📝</div>
          <p class="empty-text">本周暂无训练计划</p>
        </div>
        <div v-else class="weekly-list">
          <div
            v-for="(plan, index) in weeklyPlans"
            :key="index"
            class="plan-item"
            @click="openEditModal(plan)"
          >
            <div class="plan-date">{{ formatDate(plan.date) }}</div>
            <div class="plan-content">
              <div class="plan-project">{{ plan.project }}</div>
              <div class="plan-target">
                目标：{{ plan.target }}个
                <span v-if="plan.actualCount > 0" class="actual-count">
                  / 实际：{{ plan.actualCount }}个
                </span>
              </div>
              <div v-if="plan.note" class="plan-note">{{ plan.note }}</div>
            </div>
            <div class="plan-status" :class="getPlanStatusClass(plan)">
              {{ getPlanStatusText(plan) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 帮助说明弹窗 -->
    <div class="modal-overlay" v-if="showHelpModal" @click="showHelpModal = false">
      <div class="modal-content help-modal" @click.stop>
        <button class="close-btn" @click="showHelpModal = false">✕</button>

        <h2 class="modal-title">📊 折线图使用说明</h2>

        <div class="help-content">
          <div class="help-section">
            <h3 class="help-subtitle">功能介绍</h3>
            <p class="help-text">
              折线图展示您每周的引体向上训练目标数量趋势，帮助您直观了解训练计划的安排情况。
            </p>
          </div>

          <div class="help-section">
            <h3 class="help-subtitle">如何使用</h3>
            <ul class="help-list">
              <li><strong>查看本周数据：</strong>图表默认显示本周（周日至周六）的训练计划</li>
              <li><strong>切换周次：</strong>点击"上周"/"下周"按钮可以查看不同周的数据</li>
              <li><strong>数据来源：</strong>图表数据来自您创建的训练计划中的目标数量</li>
              <li>
                <strong>折线含义：</strong>蓝色折线连接每天的目标数量，帮助您看出训练强度的变化
              </li>
            </ul>
          </div>

          <div class="help-section">
            <h3 class="help-subtitle">图表说明</h3>
            <ul class="help-list">
              <li><strong>横轴（X轴）：</strong>显示一周七天（周日到周六）</li>
              <li><strong>纵轴（Y轴）：</strong>显示训练目标数量</li>
              <li><strong>数据点：</strong>蓝色圆点表示当天的目标数量</li>
              <li><strong>数字标签：</strong>数据点上方显示具体的目标个数</li>
            </ul>
          </div>

          <div class="help-section">
            <h3 class="help-subtitle">温馨提示</h3>
            <p class="help-text">
              💡 建议合理安排训练强度，循序渐进。如果某天没有训练计划，图表会显示为0。
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑计划弹窗 -->
    <div class="modal-overlay" v-if="showEditModal" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeEditModal">✕</button>

        <h2 class="modal-title">编辑训练计划</h2>

        <div class="modal-form">
          <div class="form-row">
            <label class="form-label">日期</label>
            <input type="text" :value="editForm.date" class="form-input" disabled />
          </div>

          <div class="form-row">
            <label class="form-label">训练项目</label>
            <input type="text" :value="editForm.project" class="form-input" disabled />
          </div>

          <div class="form-row">
            <label class="form-label">目标数量</label>
            <input type="number" v-model="editForm.target" class="form-input" />
          </div>

          <div class="form-row">
            <label class="form-label">实际完成数量</label>
            <input
              type="number"
              v-model.number="editForm.actualCount"
              placeholder="填写实际完成的个数"
              class="form-input"
              min="0"
            />
            <span class="form-hint">填写后将自动标记为已完成</span>
          </div>

          <div class="form-row">
            <label class="form-label">完成状态</label>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="editForm.completed"
                  class="checkbox-input"
                  :disabled="editForm.actualCount > 0"
                />
                <span>已完成</span>
              </label>
            </div>
          </div>

          <div class="form-row">
            <label class="form-label">备注说明</label>
            <textarea v-model="editForm.note" class="form-textarea" rows="3"></textarea>
          </div>

          <div class="modal-actions">
            <button class="btn-cancel" @click="closeEditModal">取消</button>
            <button class="btn-delete" @click="deletePlan">删除</button>
            <button class="btn-submit" @click="savePlan">保存</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'

const activeTab = ref('练习次数趋势')
const timeRange = ref('week')
const currentWeekOffset = ref(0) // 0表示本周，-1表示上周，1表示下周

// 图表配置
const chartWidth = 600
const chartHeight = 200
const chartPadding = 20

// API配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

// 获取token
const getToken = () => {
  return localStorage.getItem('token') || ''
}

// ============ API 数据类型定义 ============

export interface PlanItem {
  id?: number
  date: string
  project: string
  target: string
  note: string
  completed: boolean
  actualCount: number
}

// 创建训练计划 - 请求参数
export interface CreatePlanRequest {
  date: string
  project: string
  target: string
  note: string
}

// 创建训练计划 - 响应
export interface CreatePlanResponse {
  code: number
  message: string
  data: PlanItem
}

// 获取训练计划列表 - 请求参数
export interface GetPlanListRequest {
  timeRange?: string
  keyword?: string
}

// 获取训练计划列表 - 响应
export interface GetPlanListResponse {
  code: number
  message: string
  data: {
    list: PlanItem[]
    total: number
  }
}

// 更新训练计划 - 请求参数
export interface UpdatePlanRequest {
  target?: string
  note?: string
  actualCount?: number
  completed?: boolean
}

// 更新训练计划 - 响应
export interface UpdatePlanResponse {
  code: number
  message: string
  data: PlanItem
}

// 删除训练计划 - 响应
export interface DeletePlanResponse {
  code: number
  message: string
}

// 获取训练日期 - 请求参数
export interface GetTrainedDatesRequest {
  year: number
  month: number
}

// 获取训练日期 - 响应
export interface GetTrainedDatesResponse {
  code: number
  message: string
  data: string[]
}

// 获取训练统计 - 请求参数
export interface GetStatisticsRequest {
  timeRange?: string
}

// 获取训练统计 - 响应
export interface GetStatisticsResponse {
  code: number
  message: string
  data: {
    totalPlans: number
    completedPlans: number
    completionRate: number
    weeklyData: Array<{
      date: string
      count: number
    }>
  }
}

// 训练计划列表
const plansList = ref<PlanItem[]>([])
const loading = ref(false)

// ============ API 调用函数 ============

// 日期格式化函数
const formatDateString = (dateStr: string): string => {
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 获取训练计划列表
const fetchPlanList = async () => {
  const token = getToken()
  if (!token) return

  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/api/training-plan/list`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) throw new Error('获取计划列表失败')

    const result: GetPlanListResponse = await response.json()
    if (result.code === 200) {
      // 格式化日期
      plansList.value = result.data.list.map((item) => ({
        ...item,
        date: formatDateString(item.date),
      }))
    }
  } catch (error) {
    console.error('获取计划列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 计划表单
const planForm = reactive({
  date: '',
  project: '',
  target: '',
  note: '',
})

// 帮助弹窗
const showHelpModal = ref(false)

// 编辑弹窗
const showEditModal = ref(false)
const editingPlan = ref<PlanItem | null>(null)
const editForm = reactive({
  date: '',
  project: '',
  target: '',
  note: '',
  completed: false,
  actualCount: 0,
})

// 计算统计数据
const totalPlans = computed(() => plansList.value.length)
const completedPlans = computed(() => plansList.value.filter((p) => p.completed).length)
const completionRate = computed(() => {
  if (totalPlans.value === 0) return '0.0'
  return ((completedPlans.value / totalPlans.value) * 100).toFixed(1)
})

// 根据时间范围过滤计划
const filteredPlans = computed(() => {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  let startDate: Date
  let endDate: Date

  switch (timeRange.value) {
    case 'week': {
      // 本周：从本周日到本周六
      startDate = new Date(now)
      startDate.setDate(now.getDate() - now.getDay())
      startDate.setHours(0, 0, 0, 0)

      endDate = new Date(startDate)
      endDate.setDate(startDate.getDate() + 7)
      endDate.setHours(0, 0, 0, 0)
      break
    }
    case 'month': {
      // 本月：从本月1号到下月1号
      startDate = new Date(now.getFullYear(), now.getMonth(), 1)
      startDate.setHours(0, 0, 0, 0)

      endDate = new Date(now.getFullYear(), now.getMonth() + 1, 1)
      endDate.setHours(0, 0, 0, 0)
      break
    }
    case 'threeMonths': {
      // 近三月：从三个月前的1号到下月1号
      startDate = new Date(now.getFullYear(), now.getMonth() - 3, 1)
      startDate.setHours(0, 0, 0, 0)

      endDate = new Date(now.getFullYear(), now.getMonth() + 1, 1)
      endDate.setHours(0, 0, 0, 0)
      break
    }
    case 'halfYear': {
      // 半年内：从六个月前的1号到下月1号
      startDate = new Date(now.getFullYear(), now.getMonth() - 6, 1)
      startDate.setHours(0, 0, 0, 0)

      endDate = new Date(now.getFullYear(), now.getMonth() + 1, 1)
      endDate.setHours(0, 0, 0, 0)
      break
    }
    case 'all': {
      return plansList.value
    }
    default:
      startDate = new Date(0)
      endDate = new Date(now.getFullYear(), now.getMonth() + 1, 1)
  }

  return plansList.value.filter((plan) => {
    const planDate = new Date(plan.date + 'T00:00:00') // 添加时间部分避免时区问题
    return planDate >= startDate && planDate < endDate
  })
})

// 过滤范围内已完成的计划数
const filteredCompletedCount = computed(() => {
  return filteredPlans.value.filter((p) => p.completed).length
})

// 获取本周计划（使用与图表相同的周计算逻辑）
const weeklyPlans = computed(() => {
  const { weekStart, weekEnd } = getCurrentWeekRange()

  // 只显示当前查看周的计划
  return plansList.value.filter((plan) => {
    const planDate = new Date(plan.date + 'T00:00:00') // 添加时间部分避免时区问题
    return planDate >= weekStart && planDate < weekEnd
  })
})

// 获取当前显示周的起止日期
const getCurrentWeekRange = () => {
  const now = new Date()
  const weekStart = new Date(now)
  weekStart.setDate(now.getDate() - now.getDay() + currentWeekOffset.value * 7)
  weekStart.setHours(0, 0, 0, 0)

  const weekEnd = new Date(weekStart)
  weekEnd.setDate(weekStart.getDate() + 7)

  return { weekStart, weekEnd }
}

// 当前周标签
const currentWeekLabel = computed(() => {
  const { weekStart, weekEnd } = getCurrentWeekRange()
  const startMonth = weekStart.getMonth() + 1
  const startDay = weekStart.getDate()
  const endMonth = weekEnd.getMonth() + 1
  const endDay = weekEnd.getDate() - 1

  if (currentWeekOffset.value === 0) {
    return `本周 (${startMonth}/${startDay} - ${endMonth}/${endDay})`
  }
  return `${startMonth}/${startDay} - ${endMonth}/${endDay}`
})

// 是否是当前周
const isCurrentWeek = computed(() => currentWeekOffset.value >= 0)

// 获取本周每天的数据
const weekData = computed(() => {
  const { weekStart } = getCurrentWeekRange()
  const data = []
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

  for (let i = 0; i < 7; i++) {
    const date = new Date(weekStart)
    date.setDate(weekStart.getDate() + i)

    // 使用本地日期格式，避免时区问题
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const dateStr = `${year}-${month}-${day}`

    // 查找该日期的引体向上计划
    const plan = plansList.value.find((p) => p.date === dateStr && p.project.includes('引体向上'))

    // 优先使用实际完成数量，如果没有则使用目标数量
    const actualCount = plan?.actualCount || 0
    const count = plan ? (actualCount > 0 ? actualCount : parseInt(plan.target) || 0) : 0

    data.push({
      label: weekDays[i],
      date: dateStr,
      count: count,
    })
  }

  return data
})

// Y轴刻度
const yAxisTicks = computed(() => {
  const maxCount = Math.max(...weekData.value.map((d) => d.count), 10)
  const step = Math.ceil(maxCount / 5)
  const ticks = []
  for (let i = 0; i <= 5; i++) {
    ticks.push(step * i)
  }
  return ticks.reverse()
})

// 获取Y坐标
const getYPosition = (value: number) => {
  const maxValue = yAxisTicks.value[0]??10
  const ratio = value / maxValue
  return chartHeight - ratio * (chartHeight - chartPadding * 2) - chartPadding
}

// 获取X坐标
const getXPosition = (index: number) => {
  const step = chartWidth / 7
  return step * index + step / 2
}

// 折线路径点
const linePoints = computed(() => {
  return weekData.value
    .map((point, index) => `${getXPosition(index)},${getYPosition(point.count)}`)
    .join(' ')
})

// 切换周
const prevWeek = () => {
  currentWeekOffset.value--
}

const nextWeek = () => {
  if (!isCurrentWeek.value) {
    currentWeekOffset.value++
  }
}

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const weekDay = weekDays[date.getDay()]
  return `${month}月${day}日 ${weekDay}`
}

// 获取计划状态文本
const getPlanStatusText = (plan: PlanItem) => {
  const actualCount = plan.actualCount || 0
  if (actualCount === 0) {
    return '未完成'
  }

  const target = parseInt(plan.target) || 0
  if (target === 0) {
    return '已完成'
  }

  if (actualCount >= target) {
    return '已完成'
  }

  const percentage = Math.round((actualCount / target) * 100)
  return `完成${percentage}%`
}

// 获取计划状态样式类
const getPlanStatusClass = (plan: PlanItem) => {
  const actualCount = plan.actualCount || 0
  if (actualCount === 0) {
    return 'pending'
  }

  const target = parseInt(plan.target) || 0
  if (target === 0 || actualCount >= target) {
    return 'completed'
  }

  return 'partial'
}

// 重置表单
const resetForm = () => {
  planForm.date = ''
  planForm.project = ''
  planForm.target = ''
  planForm.note = ''
}

// 提交计划
const submitPlan = async () => {
  if (!planForm.date || !planForm.project || !planForm.target) {
    alert('请填写必填项：日期、训练项目和目标数量')
    return
  }

  const token = getToken()
  if (!token) {
    alert('请先登录')
    return
  }

  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/api/training-plan`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        date: planForm.date,
        project: planForm.project,
        target: planForm.target,
        note: planForm.note,
      }),
    })

    if (!response.ok) throw new Error('创建计划失败')

    const result: CreatePlanResponse = await response.json()
    if (result.code === 200) {
      // 格式化日期并添加到本地列表
      const newPlan = {
        ...result.data,
        date: formatDateString(result.data.date),
      }
      plansList.value.push(newPlan)
      alert('训练计划创建成功！')
      resetForm()
    } else {
      alert(result.message || '创建失败')
    }
  } catch (error) {
    console.error('创建计划失败:', error)
    alert('创建计划失败，请重试')
  } finally {
    loading.value = false
  }
}

// 打开编辑弹窗
const openEditModal = (plan: PlanItem) => {
  editingPlan.value = plan
  editForm.date = plan.date
  editForm.project = plan.project
  editForm.target = plan.target
  editForm.note = plan.note
  editForm.completed = plan.completed
  editForm.actualCount = plan.actualCount || 0
  showEditModal.value = true
}

// 关闭编辑弹窗
const closeEditModal = () => {
  showEditModal.value = false
  editingPlan.value = null
}

// 保存修改
const savePlan = async () => {
  if (!editingPlan.value) return

  editingPlan.value.target = editForm.target
  editingPlan.value.note = editForm.note
  editingPlan.value.actualCount = editForm.actualCount

  // 根据实际完成数量自动设置完成状态
  const target = parseInt(editForm.target) || 0
  if (editForm.actualCount >= target && editForm.actualCount > 0) {
    // 实际数量达到或超过目标，标记为已完成
    editingPlan.value.completed = true
  } else if (editForm.actualCount > 0) {
    // 有实际数量但未达到目标，标记为部分完成（也算已完成）
    editingPlan.value.completed = true
  } else {
    // 没有实际数量，使用手动设置的状态
    editingPlan.value.completed = editForm.completed
  }

  const token = getToken()
  const planId = editingPlan.value.id

  if (!token || !planId) {
    alert('更新失败：缺少必要信息')
    return
  }

  const updateData = {
    target: editForm.target,
    note: editForm.note,
    actualCount: editForm.actualCount,
    completed: editingPlan.value.completed,
  }



  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/api/training-plan/${planId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData),
    })

    const result: UpdatePlanResponse = await response.json()


    if (result.code === 200) {
      // 格式化日期并更新本地数据
      const updatedData = {
        ...result.data,
        date: formatDateString(result.data.date),
      }
      Object.assign(editingPlan.value, updatedData)
      alert('计划已更新！')
      closeEditModal()
    } else {
      alert(`更新失败: ${result.message}`)
    }
  } catch (error) {
    console.error('更新计划失败:', error)
    alert(`更新计划失败: ${error}`)
  } finally {
    loading.value = false
  }
}

// 删除计划
const deletePlan = async () => {
  if (!editingPlan.value) return

  if (!confirm('确定要删除这个训练计划吗？')) return

  const token = getToken()
  const planId = editingPlan.value.id

  if (!token || !planId) {
    alert('删除失败：缺少必要信息')
    return
  }

  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/api/training-plan/${planId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) throw new Error('删除计划失败')

    const result: DeletePlanResponse = await response.json()
    if (result.code === 200) {
      // 从本地列表删除
      const index = plansList.value.indexOf(editingPlan.value)
      if (index > -1) {
        plansList.value.splice(index, 1)
      }
      alert('计划已删除！')
      closeEditModal()
    } else {
      alert(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除计划失败:', error)
    alert('删除计划失败，请重试')
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  fetchPlanList()
})
</script>

<style scoped>
.train-wrapper {
  display: flex;
  gap: 20px;
  padding: 20px;
}

/* 左侧训练数据统计 */
.train-stats {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.help-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid #dcdfe6;
  background: #fff;
  color: #909399;
  cursor: pointer;
  font-size: 14px;
}

.help-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.chart-section {
  margin-bottom: 30px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.chart-tabs {
  flex: 1;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: none;
  color: #606266;
  cursor: pointer;
  font-size: 14px;
  position: relative;
}

.tab-btn.active {
  color: #409eff;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #409eff;
}

.week-nav {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 10px;
}

.week-btn {
  padding: 4px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  color: #606266;
  font-size: 13px;
  cursor: pointer;
}

.week-btn:hover:not(:disabled) {
  color: #409eff;
  border-color: #409eff;
}

.week-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.week-label {
  font-size: 13px;
  color: #606266;
  min-width: 150px;
  text-align: center;
}

.chart-container {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
}

.line-chart {
  width: 100%;
  display: flex;
  gap: 20px;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 0;
}

.y-tick {
  font-size: 12px;
  color: #909399;
  text-align: right;
  min-width: 30px;
}

.chart-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart-svg {
  width: 100%;
  height: 200px;
}

.grid-line {
  stroke: #ebeef5;
  stroke-width: 1;
}

.chart-line {
  fill: none;
  stroke: #409eff;
  stroke-width: 2;
}

.chart-point {
  fill: #409eff;
  stroke: #fff;
  stroke-width: 2;
}

.chart-label {
  fill: #303133;
  font-size: 12px;
  text-anchor: middle;
  font-weight: 500;
}

.chart-x-axis {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.x-label {
  font-size: 12px;
  color: #909399;
  text-align: center;
  flex: 1;
}

.chart-placeholder {
  text-align: center;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.chart-text {
  color: #909399;
  font-size: 14px;
}

.plan-setting-section {
  margin-top: 30px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.plan-form {
  background: #fafafa;
  padding: 20px;
  border-radius: 8px;
}

.form-row {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #409eff;
}

.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-textarea:focus {
  border-color: #409eff;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-cancel,
.btn-submit {
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #fff;
  border: 1px solid #dcdfe6;
  color: #606266;
}

.btn-cancel:hover {
  color: #409eff;
  border-color: #409eff;
}

.btn-submit {
  background: #409eff;
  border: none;
  color: #fff;
}

.btn-submit:hover {
  background: #66b1ff;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-text {
  color: #909399;
  font-size: 14px;
}

/* 右侧训练计划统计 */
.plan-stats {
  width: 480px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.plan-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 30px;
}

.stat-card {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.card-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.card-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.monthly-stats {
  margin-bottom: 30px;
}

.month-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.month-tab {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  color: #606266;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.month-tab:hover {
  color: #409eff;
  border-color: #409eff;
}

.month-tab.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.monthly-empty {
  padding: 40px 20px;
  text-align: center;
  background: #fafafa;
  border-radius: 8px;
}

.monthly-data {
  background: #fafafa;
  border-radius: 8px;
  padding: 16px;
}

.data-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.summary-item {
  text-align: center;
}

.summary-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.summary-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.summary-value.completed {
  color: #52c41a;
}

.summary-value.pending {
  color: #faad14;
}

.data-list {
  max-height: 200px;
  overflow-y: auto;
}

.data-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.data-item:last-child {
  border-bottom: none;
}

.item-date {
  font-size: 12px;
  color: #909399;
  min-width: 80px;
}

.item-project {
  flex: 1;
  font-size: 13px;
  color: #606266;
}

.item-status {
  font-size: 16px;
  color: #dcdfe6;
}

.item-status.completed {
  color: #52c41a;
}

.weekly-plan {
  margin-top: 30px;
}

.weekly-empty {
  padding: 40px 20px;
  text-align: center;
  background: #fafafa;
  border-radius: 8px;
}

.weekly-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.plan-item {
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  cursor: pointer;
  transition: all 0.2s;
}

.plan-item:hover {
  background: #e6f0ff;
  transform: translateX(4px);
}

.plan-date {
  font-size: 13px;
  color: #909399;
  min-width: 80px;
  flex-shrink: 0;
}

.plan-content {
  flex: 1;
}

.plan-project {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.plan-target {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
}

.actual-count {
  color: #52c41a;
  font-weight: 500;
  margin-left: 8px;
}

.plan-note {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.plan-status {
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 4px;
  flex-shrink: 0;
  font-weight: 500;
}

.plan-status.pending {
  background: #fff7e6;
  color: #faad14;
}

.plan-status.completed {
  background: #e6f7e6;
  color: #52c41a;
}

.plan-status.partial {
  background: #e6f0ff;
  color: #409eff;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  color: #909399;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f5f7fa;
  color: #606266;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 24px;
  padding-right: 40px;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.checkbox-group {
  padding: 10px 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-delete {
  padding: 10px 24px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
  border: 1px solid #f56c6c;
  color: #f56c6c;
  margin-right: auto;
}

.btn-delete:hover {
  background: #f56c6c;
  color: #fff;
}

/* 帮助弹窗样式 */
.help-modal {
  max-width: 600px;
}

.help-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.help-section {
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.help-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.help-subtitle {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.help-text {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
  margin: 0;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.help-list li {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  padding-left: 20px;
  position: relative;
}

.help-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #409eff;
  font-weight: bold;
}

.help-list li strong {
  color: #303133;
  font-weight: 500;
}
</style>
