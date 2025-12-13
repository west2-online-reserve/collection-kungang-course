<template>
  <div class="main">
      <NavBar
      :nav-items="navBarProps.navItems"
      :user="navBarProps.user"
      :current-page="navBarProps.currentPage"
      @logout="handleLogout"
      @menu-click="handleMenu_click"
      @page-change="handlePageChange"
      />

    <hr>

    <div>
    <!-- 你的主页内容 -->

    <!-- 反馈弹窗 -->
    <FeedbackModal
      v-model:visible="showFeedback"
      @submitted="handleFeedbackSubmitted"
    />
  </div>



    <div class="container py-5">
      <br>
      <KeepAlive :include="['Home']">
        <component
      :is="currentPageComponent"
      v-bind="componentProps"
      :key="currentPage"
      />
      </KeepAlive>


    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted , computed,reactive} from 'vue';


// 组件导入
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import NavBar from '@/components/main/layout/NavBar.vue';
import FeedbackModal from '@/components/main/layout/FeedBack.vue';
import type{ NavItem,NavBarProps,UserData } from '@/types/nav.ts';

import { useRouter } from 'vue-router';
import { authAPI } from '@/utils/api';
import Home from '@/components/main/layout/HomeComponent.vue';
import History from '@/components/main/layout/HistoryComponent.vue';
import Train from '@/components/main/layout/TrainComponent.vue';
import type { ComponentPropsMap } from '@/types/main'

//feedback
const handleFeedbackSubmitted = (data: { content: string; email?: string }) => {
  console.log('收到反馈数据:', data)
  // 这里可以处理反馈数据，比如发送到服务器等
}
// 响应式数据
const NavItems = reactive<NavItem[]>([
  { id: 1, name: '首页', page: 'home' },
  { id: 2, name: '历史记录', page: 'history' },
  { id: 3, name: '训练计划', page: 'train' }
])

const userData = ref<UserData>({
  name: '',
})

const currentPage = ref('home')


const navBarProps = computed<NavBarProps>(() => ({
  navItems: NavItems,
  user: userData.value,          // 在 computed 中会自动追踪变化
  currentPage: currentPage.value
}))




const componentProps = computed(() => {
  const propsMap: ComponentPropsMap = {
    home: {
      username: userData.value.name,

    },
    history: {

    },
    train:{


    }
  }
  const cpg=currentPage.value

  // 返回当前页面对应的 props
  return propsMap[cpg as keyof ComponentPropsMap]
})
// 当前用户信息
const showFeedback = ref<boolean>(false);
const router = useRouter();





const checkAuthStatus = async () => {
  const token = localStorage.getItem('token');

  if (!token) {
    router.push('/login');
    return;
  }

  try {
    const data=await authAPI.verifyToken(token);
    userData.value.name=data.username;

    const newtoken=(await authAPI.refreshToken(token)).data.token;
    localStorage.setItem('token', newtoken);

    // Token有效，跳转到主页
    // router.push('/main');
  } catch (error) {
    console.error('Token验证失败:', error);
    // 清除无效的token
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  }
};

const handleMenu_click = (action: string) => {
  if (action === 'profile') {
    router.push('/profile');
  } else if (action === 'feedback') {
    showFeedback.value = true;
  }
};



// 处理页面切换
const handlePageChange = (page:string) => {

  currentPage.value = page;

};




// 根据currentPage动态计算对应的组件
const currentPageComponent = computed(() => {

  switch (navBarProps.value.currentPage) {
    case 'home':
      return Home;
    case 'history':

      return History;
    case 'train':

      return Train;
    default:
      return Home;
  }

});

// 事件处理
const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
  // window.location.href = 'login.html';
};



// 初始化
onMounted(() => {

});
await checkAuthStatus();
</script>

<style scoped>
/* 原有的样式可以保留在这里 */
.main {
  background-color: #f0f7ee;
  min-height: 100vh;
  min-width: 100vw;
  font-family: 'Segoe UI', Roboto, sans-serif;
}

.feature-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  height: 100%;
  background-color: #ffffff;
}

.card-header {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  color: white;
  border-bottom: none;
}

.btn-primary {
  background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
  border: none;
}

.feature-icon {
  font-size: 2.5rem;
  color: #4caf50;
  margin-bottom: 15px;
}

.stat-card {
  background-color: #f1f8e9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  border-left: 4px solid #4caf50;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2e7d32;
}

.stat-label {
  color: #555;
  font-size: 0.9rem;
}

.history-record {
  border-bottom: 1px solid #e9ecef;
  padding: 12px 0;
}

.history-record:last-child {
  border-bottom: none;
}

.chart-container {
  height: 300px;
  position: relative;
}

.progress-bar {
  background: linear-gradient(90deg, #4caf50 0%, #2e7d32 100%);
}

.plan-status-badge {
  padding: 0.35em 0.65em;
}
</style>
