<template>
  <div class="min-h-screen bg-[#fff8e1] flex items-center justify-center p-4 font-sans">
    <div class="max-w-6xl w-full mx-auto">
      <!-- 标题区域 -->
      <div class="text-center mb-8">
        <h1 class="text-5xl font-extrabold text-[#5d4037] mb-2 tracking-wide drop-shadow-sm">
          合成大福州
        </h1>
        <p class="text-[#8d6e63] text-lg">物理合成 · 挑战高分 · 实时榜单</p>
      </div>

      <!-- 主体卡片容器 -->
      <div
        class="bg-white rounded-3xl shadow-2xl overflow-hidden border-4 border-[#ffe082] flex flex-col lg:flex-row"
      >
        <!-- 左侧：游戏区域 (自适应) -->
        <div
          class="relative bg-[#fff6d6] lg:w-[500px] flex-shrink-0 flex flex-col border-b lg:border-b-0 lg:border-r border-[#ffe082]"
        >
          <!-- 顶部信息栏 -->
          <div
            class="absolute top-4 left-0 w-full px-6 flex justify-between items-center z-10 pointer-events-none"
          >
            <div
              class="bg-white/90 backdrop-blur text-[#5d4037] px-4 py-2 rounded-full font-bold shadow-sm border border-amber-200"
            >
              当前分数: <span class="text-amber-600 text-xl">{{ currentScore }}</span>
            </div>
            <div
              class="bg-white/90 backdrop-blur text-[#5d4037] px-4 py-2 rounded-full font-bold shadow-sm border border-amber-200"
            >
              下个水果:
              <span
                class="inline-block w-4 h-4 rounded-full align-middle ml-1"
                :style="{ backgroundColor: nextFruitColor }"
              ></span>
            </div>
          </div>

          <!-- 游戏画布容器 -->
          <div
            ref="gameWrapper"
            class="flex-1 flex justify-center items-center p-4 overflow-hidden relative min-h-[600px] lg:min-h-[800px]"
          >
            <!-- Canvas 将被挂载在这里 -->
            <div id="game-container" class="shadow-xl rounded-lg overflow-hidden"></div>

            <!-- 游戏结束遮罩 -->
            <div
              v-if="isGameOver"
              class="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col justify-center items-center z-20 text-white animate-fade-in"
            >
              <h2 class="text-4xl font-bold mb-2">游戏结束!</h2>
              <p class="text-xl mb-8">
                最终得分: <span class="text-amber-400 font-bold text-3xl">{{ currentScore }}</span>
              </p>

              <div class="flex flex-col gap-3 w-48">
                <button
                  @click="restartGame"
                  class="w-full py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold transition transform hover:scale-105 shadow-lg"
                >
                  再来一局
                </button>
                <button
                  @click="submitScore"
                  :disabled="isSubmitting || currentScore <= 0"
                  class="w-full py-3 bg-white text-amber-800 hover:bg-gray-100 rounded-xl font-bold transition transform hover:scale-105 shadow-lg disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {{ isSubmitting ? '提交中...' : '提交成绩' }}
                </button>
              </div>

              <!-- 提交状态提示 -->
              <div
                v-if="submitStatus"
                class="mt-4 px-4 py-2 rounded bg-black/40 text-sm"
                :class="submitStatus.type === 'success' ? 'text-green-300' : 'text-red-300'"
              >
                {{ submitStatus.message }}
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：排行榜与操作面板 -->
        <div class="flex-1 bg-gradient-to-br from-white to-amber-50 p-6 lg:p-10 flex flex-col">
          <!-- 用户信息 -->
          <div class="bg-white rounded-2xl p-6 shadow-sm border border-amber-100 mb-6">
            <h3 class="text-lg font-bold text-[#5d4037] mb-4 flex items-center">
              <span class="w-1 h-6 bg-amber-500 rounded-full mr-3"></span>
              我的战绩
            </h3>
            <div class="flex justify-between items-end">
              <div>
                <p class="text-gray-500 text-sm">玩家</p>
                <p class="font-medium text-[#5d4037]">{{ player.name }}</p>
              </div>
              <div class="text-right">
                <p class="text-gray-500 text-sm">历史最高</p>
                <p class="text-3xl font-bold text-amber-600">{{ personal.top5[0]?.score || 0 }}</p>
              </div>
            </div>
          </div>

          <!-- 排行榜 Tabs -->
          <div
            class="flex-1 flex flex-col bg-white rounded-2xl shadow-sm border border-amber-100 overflow-hidden"
          >
            <div class="flex border-b border-amber-100">
              <button
                class="flex-1 py-4 text-center font-bold transition-colors relative"
                :class="
                  activeTab === 'global'
                    ? 'text-amber-700 bg-amber-50/50'
                    : 'text-gray-400 hover:text-amber-600'
                "
                @click="activeTab = 'global'"
              >
                全网排行
                <div
                  v-if="activeTab === 'global'"
                  class="absolute bottom-0 left-0 w-full h-1 bg-amber-500"
                ></div>
              </button>
              <button
                class="flex-1 py-4 text-center font-bold transition-colors relative"
                :class="
                  activeTab === 'personal'
                    ? 'text-amber-700 bg-amber-50/50'
                    : 'text-gray-400 hover:text-amber-600'
                "
                @click="activeTab = 'personal'"
              >
                个人记录
                <div
                  v-if="activeTab === 'personal'"
                  class="absolute bottom-0 left-0 w-full h-1 bg-amber-500"
                ></div>
              </button>
            </div>

            <!-- 列表内容 -->
            <div class="flex-1 overflow-y-auto p-2 scrollbar-thin">
              <!-- 全网榜单 -->
              <div v-if="activeTab === 'global'" class="space-y-2">
                <div v-if="globalTop.length === 0" class="text-center py-10 text-gray-400">
                  暂无数据
                </div>
                <div
                  v-for="(item, idx) in globalTop"
                  :key="`${item.id}-${item.time}`"
                  class="flex items-center p-3 rounded-xl hover:bg-amber-50 transition-colors"
                >
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center font-bold mr-4 text-sm"
                    :class="[
                      idx === 0
                        ? 'bg-yellow-400 text-yellow-900'
                        : idx === 1
                          ? 'bg-gray-300 text-gray-800'
                          : idx === 2
                            ? 'bg-orange-300 text-orange-900'
                            : 'bg-gray-100 text-gray-500',
                    ]"
                  >
                    {{ idx + 1 }}
                  </div>
                  <div class="flex-1">
                    <div class="font-medium text-gray-800 text-sm">{{ item.name }}</div>
                    <div class="text-xs text-gray-400">{{ formatDate(item.time) }}</div>
                  </div>
                  <div class="font-bold text-amber-600">{{ item.score }}</div>
                </div>
              </div>

              <!-- 个人榜单 -->
              <div v-if="activeTab === 'personal'" class="space-y-2">
                <div v-if="personal.top5.length === 0" class="text-center py-10 text-gray-400">
                  快开始游戏创造记录吧！
                </div>
                <div
                  v-for="(item, idx) in personal.top5"
                  :key="idx"
                  class="flex items-center justify-between p-3 rounded-xl hover:bg-amber-50 transition-colors border-l-4 border-transparent hover:border-amber-400"
                >
                  <div class="flex items-center">
                    <span class="text-gray-400 text-sm w-8 text-center">第{{ idx + 1 }}</span>
                    <div class="ml-4">
                      <div class="text-xs text-gray-400">{{ formatDate(item.time) }}</div>
                    </div>
                  </div>
                  <span class="font-bold text-amber-700 text-lg">{{ item.score }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-4 text-center text-xs text-gray-400">点击屏幕上方区域释放水果</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { getApiUrl, API_ENDPOINTS } from '@/config/api'

// ===================== 类型定义 =====================
/** 玩家信息 */
interface PlayerInfo {
  id: string
  name: string
}

/** 榜单条目 */
interface RankItem {
  id: string
  name: string
  score: number
  time: number
}

/** 个人榜单数据 */
interface PersonalRank {
  lastScore: number | null
  top5: { score: number; time: number }[]
}

/** 提交状态 */
interface SubmitStatus {
  type: 'success' | 'error'
  message: string
}

// ================= 配置区域 =================
/**
 * 水果配置表
 * 如何替换图片：
 * 1. 找到对应的水果级别 (level 0 是葡萄，level 1 是樱桃...)
 * 2. 在 img 字段中填入图片的 URL（可以是本地 /assets/xxx.png 或网络图片 https://...）
 * 3. 建议图片为透明背景的 PNG，且长宽相等（正方形）
 * 4. 如果 img 留空，系统会自动使用 color 字段的颜色绘制圆球
 */
const FRUITS = [
  { level: 0, radius: 20, color: '#9e00eb', score: 2, img: '' }, // 葡萄
  { level: 1, radius: 30, color: '#ff5454', score: 4, img: '' }, // 樱桃
  { level: 2, radius: 42, color: '#ffbd14', score: 6, img: '' }, // 橘子
  { level: 3, radius: 54, color: '#ffec27', score: 8, img: '' }, // 柠檬
  { level: 4, radius: 68, color: '#54ff6e', score: 10, img: '' }, // 猕猴桃
  { level: 5, radius: 82, color: '#ff5454', score: 12, img: '' }, // 西红柿
  { level: 6, radius: 98, color: '#ffccaa', score: 14, img: '' }, // 桃子
  { level: 7, radius: 115, color: '#ffd93f', score: 16, img: '' }, // 菠萝
  { level: 8, radius: 135, color: '#ff88ff', score: 18, img: '' }, // 椰子
  { level: 9, radius: 155, color: '#27ae60', score: 20, img: '' }, // 西瓜
  { level: 10, radius: 175, color: '#27ae60', score: 40, img: '' }, // 大西瓜
]

const GAME_WIDTH = 450
const GAME_HEIGHT = 800
const WALL_THICKNESS = 60
const DEAD_LINE_Y = 150

// ================= 状态管理 =================
// 游戏核心状态
const currentScore = ref(0)
const isGameOver = ref(false)
const nextFruitIndex = ref(0)

// 提交相关状态
const isSubmitting = ref(false)
const submitStatus = ref<SubmitStatus | null>(null)

// 榜单相关
const activeTab = ref('global')
const userStore = useUserStore()
const player = ref<{
  id: string
  name: string
}>({
  id: userStore.studentId || `guest-${Math.random().toString(36).slice(2, 8)}`,
  name: userStore.userName || '游客',
})
const personal = ref<PersonalRank>({ lastScore: null, top5: [] })
const globalTop = ref<RankItem[]>([])

// 计算属性：预览下一个水果的颜色（仅用于UI显示）
const nextFruitColor = computed(() => {
  const fruitData = FRUITS[nextFruitIndex.value]
  return fruitData ? fruitData.color : '#9e00eb' // 默认颜色作为后备
})

// 本地存储key
const keyPersonal = computed(() => `watermelon_personal_${player.value.id}`)
const keyGlobal = 'watermelon_global'
const keyUser = 'watermelon_user'

// 游戏核心变量
let engine: any = null
let render: any = null
let runner: any = null
let gameRunning = true
let currentFruit: any = null
let isClickable = true
let currentPointerX = GAME_WIDTH / 2
const gameWrapper = ref<HTMLElement | null>(null)

// 全局声明
declare global {
  interface Window {
    Matter: any
  }
}

// 重新声明 Matter 变量
declare const Matter: any

// ================= 游戏核心逻辑 =================

// 1. 动态加载 Matter.js
const loadMatterJS = () => {
  return new Promise((resolve, reject) => {
    if (window.Matter) {
      resolve(true)
      return
    }
    const script = document.createElement('script')
    // 使用可靠的 CDN
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js'
    script.async = true
    script.onload = () => resolve(true)
    script.onerror = (err) => reject(err)
    document.head.appendChild(script)
  })
}

// 2. 初始化游戏引擎
const initGame = async () => {
  try {
    await loadMatterJS()

    // 重置状态
    currentScore.value = 0
    isGameOver.value = false
    gameRunning = true
    isClickable = true
    nextFruitIndex.value = Math.floor(Math.random() * 5) // 初始随机
    submitStatus.value = null

    // 清理旧实例
    if (engine) {
      Matter.Runner.stop(runner)
      Matter.World.clear(engine.world)
      Matter.Engine.clear(engine)
      if (render) {
        Matter.Render.stop(render)
        render.canvas?.remove()
      }
    }

    // 创建引擎
    engine = Matter.Engine.create({ gravity: { y: 1.5 } })

    // 创建渲染器
    const container = document.getElementById('game-container')!
    // 清空容器防止重复
    container.innerHTML = ''

    render = Matter.Render.create({
      element: container,
      engine: engine,
      options: {
        width: GAME_WIDTH,
        height: GAME_HEIGHT,
        wireframes: false,
        background: 'transparent', // 透明背景，使用 CSS 控制背景色
        pixelRatio: window.devicePixelRatio,
      },
    })

    // 设置 CSS 样式以适应容器
    render.canvas.style.width = '100%'
    render.canvas.style.height = '100%'
    render.canvas.style.objectFit = 'contain'

    // 创建墙壁
    const ground = Matter.Bodies.rectangle(
      GAME_WIDTH / 2,
      GAME_HEIGHT + WALL_THICKNESS / 2,
      GAME_WIDTH,
      WALL_THICKNESS,
      { isStatic: true, render: { visible: false } },
    )
    const leftWall = Matter.Bodies.rectangle(
      -WALL_THICKNESS / 2,
      GAME_HEIGHT / 2,
      WALL_THICKNESS,
      GAME_HEIGHT * 2,
      { isStatic: true, render: { visible: false } },
    )
    const rightWall = Matter.Bodies.rectangle(
      GAME_WIDTH + WALL_THICKNESS / 2,
      GAME_HEIGHT / 2,
      WALL_THICKNESS,
      GAME_HEIGHT * 2,
      { isStatic: true, render: { visible: false } },
    )

    Matter.World.add(engine.world, [ground, leftWall, rightWall])

    // 运行
    Matter.Render.run(render)
    runner = Matter.Runner.create()
    Matter.Runner.run(runner, engine)

    bindInputEvents()
    createPendingFruit()

    // 监听碰撞和更新
    Matter.Events.on(engine, 'collisionStart', handleCollisions)
    Matter.Events.on(engine, 'afterUpdate', checkGameOver)
    Matter.Events.on(render, 'afterRender', drawGuideLines)
  } catch (err) {
    console.error('Game Init Error:', err)
  }
}

// 3. 辅助函数：生成渲染配置（支持图片）
const getRenderConfig = (fruitData: any) => {
  if (fruitData.img) {
    return {
      sprite: {
        texture: fruitData.img,
        xScale: (fruitData.radius * 2) / 200,
        yScale: (fruitData.radius * 2) / 200,
      },
    }
  } else {
    return {
      fillStyle: fruitData.color,
    }
  }
}

// 4. 创建待下落的水果
const createPendingFruit = () => {
  if (!gameRunning) return

  const index = nextFruitIndex.value
  const fruitData = FRUITS[index]
  if (!fruitData) return

  // 确保生成位置在边界内
  let spawnX = currentPointerX
  spawnX = Math.max(fruitData.radius + 10, Math.min(spawnX, GAME_WIDTH - fruitData.radius - 10))

  currentFruit = Matter.Bodies.circle(spawnX, 60, fruitData.radius, {
    isSensor: true, // 传感器模式：不发生物理碰撞
    isStatic: true, // 静态：不重力下落
    label: 'pending',
    render: getRenderConfig(fruitData),
    customData: { level: index },
  })

  Matter.World.add(engine.world, currentFruit)
  isClickable = true
}

// 5. 交互事件
const bindInputEvents = () => {
  const canvas = render.canvas

  // 坐标转换：将屏幕坐标转换为 Canvas 内部坐标
  const getCanvasX = (clientX: number) => {
    const rect = canvas.getBoundingClientRect()
    const scaleX = GAME_WIDTH / rect.width
    return (clientX - rect.left) * scaleX
  }

  const handleMove = (e: MouseEvent | TouchEvent) => {
    if (!isClickable || !currentFruit) return
    e.preventDefault()

    // 确保e.touches[0]存在
    const clientX =
      'touches' in e && e.touches.length > 0 && e.touches[0]
        ? e.touches[0].clientX
        : (e as MouseEvent).clientX
    const x = getCanvasX(clientX)

    // 限制移动范围
    const r = currentFruit.circleRadius
    currentPointerX = Math.max(r + 10, Math.min(x, GAME_WIDTH - r - 10))

    Matter.Body.setPosition(currentFruit, { x: currentPointerX, y: 60 })
  }

  const handleRelease = (e: MouseEvent | TouchEvent) => {
    e.preventDefault()
    if (!isClickable || !currentFruit || !gameRunning) return

    // 释放水果
    isClickable = false
    Matter.Body.setStatic(currentFruit, false)
    currentFruit.isSensor = false
    currentFruit.label = 'fruit'
    currentFruit.restitution = 0.2

    // 准备下一个
    currentFruit = null
    nextFruitIndex.value = Math.floor(Math.random() * 5) // 更新下一个的预览
    setTimeout(createPendingFruit, 600) // 延迟生成
  }

  // 添加点击放置功能 - 针对移动端优化
  const handleTap = (e: MouseEvent | TouchEvent) => {
    if (!isClickable || !currentFruit || !gameRunning) return
    e.preventDefault()

    // 获取点击位置的X坐标
    const clientX =
      'touches' in e && e.touches.length > 0 && e.touches[0]
        ? e.touches[0].clientX
        : (e as MouseEvent).clientX
    const x = getCanvasX(clientX)

    // 限制X坐标在游戏区域内
    const r = currentFruit.circleRadius
    const targetX = Math.max(r + 10, Math.min(x, GAME_WIDTH - r - 10))

    // 设置水果位置到点击位置
    Matter.Body.setPosition(currentFruit, { x: targetX, y: 60 })

    // 直接释放水果（模拟点击即放置）
    handleRelease(e)
  }

  canvas.addEventListener('mousemove', handleMove)
  canvas.addEventListener('touchmove', handleMove, { passive: false })
  canvas.addEventListener('mouseup', handleRelease)
  canvas.addEventListener('touchend', handleRelease)
  // 添加点击事件（针对移动端）
  canvas.addEventListener('touchstart', handleTap, { passive: false })
  // 可选：也为桌面端添加点击放置功能
  canvas.addEventListener('mousedown', handleTap)
}

// 6. 碰撞合成逻辑
const handleCollisions = (event: any) => {
  if (!gameRunning) return

  const pairs = event.pairs
  // 标记需要移除的物体，避免同一帧多次处理
  const bodiesToRemove = new Set()
  const newBodiesToAdd: any[] = []

  pairs.forEach((pair: any) => {
    const { bodyA, bodyB } = pair
    if (
      bodyA.label === 'fruit' &&
      bodyB.label === 'fruit' &&
      !bodiesToRemove.has(bodyA) &&
      !bodiesToRemove.has(bodyB)
    ) {
      if (bodyA.customData.level === bodyB.customData.level) {
        const level = bodyA.customData.level

        // 还没到最大等级
        if (level < FRUITS.length - 1) {
          bodiesToRemove.add(bodyA)
          bodiesToRemove.add(bodyB)

          const newLevel = level + 1
          const newFruitData = FRUITS[newLevel]
          if (!newFruitData) return

          const midX = (bodyA.position.x + bodyB.position.x) / 2
          const midY = (bodyA.position.y + bodyB.position.y) / 2

          const newBody = Matter.Bodies.circle(midX, midY, newFruitData.radius, {
            label: 'fruit',
            restitution: 0.2,
            render: getRenderConfig(newFruitData),
            customData: { level: newLevel },
          })

          newBodiesToAdd.push(newBody)

          // 加分
          currentScore.value += newFruitData.score
        }
      }
    }
  })

  if (bodiesToRemove.size > 0) {
    Matter.World.remove(engine.world, Array.from(bodiesToRemove))
    Matter.World.add(engine.world, newBodiesToAdd)
  }
}

// 7. 游戏结束检测
const checkGameOver = () => {
  if (!gameRunning) return

  const bodies = Matter.Composite.allBodies(engine.world)
  for (const body of bodies) {
    if (body.label === 'fruit') {
      // 只有静止且超出红线才算输
      if (body.position.y < DEAD_LINE_Y && body.velocity.y > -0.1 && body.velocity.y < 0.1) {
        // 这里加个简单的防误判：刚生成的pending水果不算
        gameRunning = false
        isGameOver.value = true
        break
      }
    }
  }
}

// 8. 绘制辅助线
const drawGuideLines = () => {
  if (!render) return
  const ctx = render.context
  ctx.save()

  // 警戒线
  ctx.beginPath()
  ctx.moveTo(0, DEAD_LINE_Y)
  ctx.lineTo(GAME_WIDTH, DEAD_LINE_Y)
  ctx.strokeStyle = '#e74c3c'
  ctx.lineWidth = 2
  ctx.setLineDash([10, 10])
  ctx.stroke()

  // 下落瞄准线
  if (isClickable && currentFruit) {
    ctx.beginPath()
    ctx.moveTo(currentFruit.position.x, currentFruit.position.y)
    ctx.lineTo(currentFruit.position.x, GAME_HEIGHT)
    ctx.strokeStyle = 'rgba(0,0,0,0.1)'
    ctx.lineWidth = 2
    ctx.setLineDash([5, 5])
    ctx.stroke()
  }

  ctx.restore()
}

// ================= 榜单和提交逻辑 =================

/** 加载用户信息 */
const loadUser = () => {
  try {
    const savedUser = localStorage.getItem(keyUser)
    if (savedUser) {
      player.value = JSON.parse(savedUser)
    } else {
      localStorage.setItem(keyUser, JSON.stringify(player.value))
    }
    // 覆盖为已登录用户信息（若存在）
    if (userStore.studentId) player.value.id = userStore.studentId
    if (userStore.userName) player.value.name = userStore.userName
  } catch (err) {
    console.error('加载用户信息失败:', err)
  }
}

// 监听userStore中用户名的变化，确保实时更新
watch(
  () => userStore.userName,
  (newName) => {
    if (newName) {
      player.value.name = newName
      // 更新本地存储
      try {
        localStorage.setItem(keyUser, JSON.stringify(player.value))
      } catch (err) {
        console.error('更新本地存储失败:', err)
      }
    }
  },
)

/** 加载榜单数据 */
const loadRanks = async () => {
  try {
    // 先尝试从后端加载全球排行榜
    const globalResponse = await fetch(getApiUrl(API_ENDPOINTS.GAME_WATERMELON_LEADERBOARD))
    if (globalResponse.ok) {
      const globalData = await globalResponse.json()
      if (globalData.success) {
        // 转换后端返回的数据格式为前端需要的格式
        // 后端返回的 time 是秒级时间戳，不需要额外转换
        globalTop.value = Array.isArray(globalData.items)
          ? globalData.items.map((item: any) => ({
              id: `user-${item.name || item.id}-${item.time}`, // 创建唯一ID
              name: item.name || `玩家${item.id}`,
              score: item.score,
              time: item.time, // 保持秒级时间戳，formatDate 会自动转换
            }))
          : []
        // 保存到本地作为备份
        localStorage.setItem(keyGlobal, JSON.stringify(globalTop.value))
      }
    }

    // 尝试从后端加载个人榜单（需要token）
    const token = localStorage.getItem('token')
    if (token) {
      const personalResponse = await fetch(getApiUrl(API_ENDPOINTS.GAME_WATERMELON_PERSONAL), {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (personalResponse.ok) {
        const personalData = await personalResponse.json()
        if (personalData.success) {
          personal.value = {
            lastScore: personalData.lastScore,
            top5: Array.isArray(personalData.top5)
              ? personalData.top5.map((item: any) => ({
                  score: typeof item === 'number' ? item : item.score,
                  // 个人榜单直接使用全球排行榜中的时间数据，确保time为number类型
                  time: (globalTop.value.find(
                    (g) => g.score === (typeof item === 'number' ? item : item.score),
                  )?.time ||
                    item.time ||
                    0) as number,
                }))
              : [],
          }
          // 保存到本地作为备份
          localStorage.setItem(keyPersonal.value, JSON.stringify(personal.value))
          return // 成功从后端加载，直接返回
        }
      }
    }

    // 后端加载失败或无token时，从本地存储加载
    const personalData = localStorage.getItem(keyPersonal.value)
    if (personalData) {
      const parsed = JSON.parse(personalData)
      // 兼容旧格式数据
      if (
        Array.isArray(parsed.top5) &&
        parsed.top5.length > 0 &&
        typeof parsed.top5[0] === 'number'
      ) {
        personal.value = {
          lastScore: parsed.lastScore,
          top5: parsed.top5.map((s: number) => ({
            score: s,
            // 从全球排行榜查找相同分数的时间
            time: (globalTop.value.find((g) => g.score === s)?.time || 0) as number,
          })),
        }
      } else {
        personal.value = {
          lastScore: parsed.lastScore || null,
          top5: Array.isArray(parsed.top5)
            ? parsed.top5.map((item: any) => ({
                score: item.score || 0,
                // 优先从全球排行榜查找相同分数的时间，确保time为number类型
                time: (globalTop.value.find((g) => g.score === (item.score || 0))?.time ||
                  item.time ||
                  0) as number,
              }))
            : [],
        }
      }
    }

    // 如果后端全球排行榜加载失败，尝试从本地加载
    if (globalTop.value.length === 0) {
      const globalData = localStorage.getItem(keyGlobal)
      if (globalData) {
        try {
          const parsed = JSON.parse(globalData)
          globalTop.value = Array.isArray(parsed) ? parsed : []
        } catch (e) {
          console.error('解析本地排行榜数据失败:', e)
          globalTop.value = []
        }
      }
    }
  } catch (err) {
    console.error('加载榜单失败:', err)
    // 错误情况下确保有默认值
    personal.value = { lastScore: null, top5: [] }
    globalTop.value = []

    // 尝试从本地恢复数据
    try {
      const personalData = localStorage.getItem(keyPersonal.value)
      const globalData = localStorage.getItem(keyGlobal)
      if (personalData) {
        const parsed = JSON.parse(personalData)
        // 兼容旧格式数据
        if (
          parsed &&
          Array.isArray(parsed.top5) &&
          parsed.top5.length > 0 &&
          typeof parsed.top5[0] === 'number'
        ) {
          personal.value = {
            lastScore: parsed.lastScore,
            top5: parsed.top5.map((s: number) => ({
              score: s,
              // 从全球排行榜查找相同分数的时间
              time: (globalTop.value.find((g) => g.score === s)?.time || 0) as number,
            })),
          }
        } else if (parsed) {
          // 确保个人榜单数据结构正确
          personal.value = {
            lastScore: parsed.lastScore || null,
            top5: Array.isArray(parsed.top5)
              ? parsed.top5.map((item: any) => ({
                  score: item.score || 0,
                  // 优先从全球排行榜查找相同分数的时间，确保time为number类型
                  time: (globalTop.value.find((g) => g.score === (item.score || 0))?.time ||
                    item.time ||
                    0) as number,
                }))
              : [],
          }
        }
      }
      if (globalData) {
        const parsedGlobal = JSON.parse(globalData)
        globalTop.value = Array.isArray(parsedGlobal) ? parsedGlobal : []
      }
    } catch (e) {
      console.error('本地数据恢复失败:', e)
    }
  }
}

/** 保存榜单数据到本地 */
const saveRanks = () => {
  try {
    localStorage.setItem(keyPersonal.value, JSON.stringify(personal.value))
    localStorage.setItem(keyGlobal, JSON.stringify(globalTop.value))
  } catch (err) {
    console.error('保存榜单失败:', err)
  }
}

// 格式化时间戳 - 统一的时间格式化方法（全球和个人榜单共用）
const formatDate = (ts?: number) => {
  // 处理undefined或无效的时间戳
  if (ts === undefined || ts === null || isNaN(ts)) {
    return '暂无时间数据'
  }

  // 处理秒级和毫秒级时间戳
  const ms = ts < 1e10 ? ts * 1000 : ts
  const date = new Date(ms)

  // 补零函数
  const pad = (n: number) => n.toString().padStart(2, '0')

  // 使用UTC时间格式化（和全球榜单保持一致）
  return `${date.getUTCFullYear()}-${pad(date.getUTCMonth() + 1)}-${pad(date.getUTCDate())} ${pad(date.getUTCHours())}:${pad(date.getUTCMinutes())}:${pad(date.getUTCSeconds())}`
}

// 重新开始游戏
const restartGame = () => {
  initGame()
}

/** 提交游戏分数到后端 + 更新本地榜单 */
const submitScore = async () => {
  // 基础验证
  if (currentScore.value <= 0 || isSubmitting.value) return

  isSubmitting.value = true
  submitStatus.value = null

  try {
    // 1. 构造提交数据（根据后端models.SubmitScoreRequest的结构）
    const submitData = {
      id: player.value.id,
      score: currentScore.value,
    }

    // 2. 调用后端API提交分数
    const token = localStorage.getItem('token')
    const response = await fetch(getApiUrl(API_ENDPOINTS.GAME_WATERMELON_SCORE), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(submitData),
    })

    const result = await response.json()

    // 3. 处理提交结果
    // 无论API是否成功，都更新本地榜单作为备份
    personal.value.lastScore = currentScore.value

    // 处理个人榜单，直接从全球排行榜查找相同分数的时间，确保time为number类型
    const newScore = {
      score: currentScore.value,
      time: (globalTop.value.find((g) => g.score === currentScore.value)?.time || 0) as number,
    }

    const scoreSet = new Set<number>()
    personal.value.top5 = [...personal.value.top5, newScore]
      .filter((item) => {
        if (scoreSet.has(item.score)) return false
        scoreSet.add(item.score)
        return true
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)

    // 4. API成功后刷新后端数据
    if (response.ok && result.success) {
      // 提交成功后重新加载榜单，确保数据最新
      await loadRanks()

      // API返回成功
      submitStatus.value = {
        type: 'success',
        message: `分数提交成功！当前分数：${currentScore.value}`,
      }
    } else {
      // API返回非成功状态，但数据已保存到本地
      submitStatus.value = {
        type: 'success',
        message: `分数已保存到本地！当前分数：${currentScore.value}。${result.Message || '服务器响应异常'}`,
      }
    }

    // 自动切到个人榜看结果
    activeTab.value = 'personal'
  } catch (err) {
    // 网络错误/API失败时，仅更新本地榜单（降级处理）
    console.error('提交分数失败:', err)

    // 本地更新榜单，使用秒级时间戳
    personal.value.lastScore = currentScore.value
    const currentTime = Math.floor(Date.now() / 1000)
    const newScore = { score: currentScore.value, time: currentTime }

    const scoreSet = new Set<number>()
    personal.value.top5 = [...personal.value.top5, newScore]
      .filter((item) => {
        if (scoreSet.has(item.score)) return false
        scoreSet.add(item.score)
        return true
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)

    // 提示错误
    submitStatus.value = {
      type: 'error',
      message: `提交失败（已保存到本地）：${(err as Error).message || '网络异常'}`,
    }
  } finally {
    isSubmitting.value = false
    // 保存本地数据
    saveRanks()
    // 3秒后清空提示
    setTimeout(() => {
      submitStatus.value = null
    }, 3000)
  }
}

// ===================== 生命周期 =====================
onMounted(async () => {
  // 加载本地数据
  loadUser()
  // 异步加载榜单数据
  await loadRanks()

  // 启动游戏
  setTimeout(initGame, 100)
})

onUnmounted(() => {
  if (runner) Matter.Runner.stop(runner)
  if (engine) Matter.Engine.clear(engine)
  if (render) {
    Matter.Render.stop(render)
    render.canvas?.remove()
  }
})
</script>

<style scoped>
/* 自定义滚动条 */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: #fff;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: #ffe082;
  border-radius: 20px;
}

/* 简单的淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

/* 强制画布块级显示 */
#game-container :deep(canvas) {
  display: block;
}

/* 按钮禁用样式 */
button:disabled {
  background-color: #d1d5db;
  cursor: not-allowed;
}
</style>
