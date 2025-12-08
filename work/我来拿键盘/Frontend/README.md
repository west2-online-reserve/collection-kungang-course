# 校园打卡系统 - 前端 (Frontend)

这是校园打卡系统的前端应用程序，使用 Vue 3 + TypeScript + Vite 构建，提供现代化、响应式的用户界面。

## 项目概述

前端部分是校园打卡系统的用户交互层，负责展示校园历史、地理位置打卡、学院互动和休闲游戏等核心功能。该应用采用组件化设计，确保代码的可维护性和可扩展性。

## 项目结构

前端应用程序遵循标准的 Vue 3 组件化架构，主要目录结构如下：

- **`src/App.vue`**: 应用程序根组件
- **`src/main.ts`**: 应用程序入口文件
- **`src/pages`**: 包含应用程序的主要视图页面
  - `Auth.vue`: 用户认证页面（登录/注册）
  - `Home.vue`: 主页
  - `HistoryMuseum.vue`: 历史博物馆页面
  - `CampusCheckin.vue`: 校园打卡页面
  - `LocationDetail.vue`: 打卡地点详情页面
  - `CollegeIntro.vue`: 学院介绍页面
  - `CollegeDetail.vue`: 学院详情页面
  - `Game.vue`: 游戏页面（合成大西瓜）
  - `EndScreen.vue`: 游戏结束页面
  - `Settings.vue`: 用户设置页面
- **`src/components`**: 可复用的 UI 组件
  - 通用组件：`TopBar.vue`, `Sidebar.vue`
  - 功能组件：认证、打卡、学院、历史、设置等相关组件
- **`src/router`**: Vue Router 配置，管理页面路由
- **`src/stores`**: Pinia 状态管理，包含用户、UI 和计数器等状态
- **`src/assets`**: 静态资源，如样式文件
- **`src/config`**: 配置文件，如 API 端点配置
- **`src/layouts`**: 布局组件，如主布局
- **`src/utils`**: 工具函数和第三方库

## 核心功能模块

### 用户认证模块
- 实现用户注册、登录功能
- 管理用户会话和 JWT 令牌
- 提供用户资料编辑功能

### 历史探索模块
- 历史事件时间轴展示
- 历史博物馆内容浏览
- 历史详情查看

### 校园打卡模块
- 打卡地点列表展示
- 地理位置打卡功能
- 评论和弹幕互动

### 学院互动模块
- 学院信息展示
- 学院相关内容评论和点赞
- 学院详情查看

### 游戏模块
- 合成大西瓜游戏实现
- 游戏排行榜功能
- 游戏结果记录

## 技术特性

- **组件化设计**: 使用 Vue 3 的组合式 API 实现高复用性组件
- **TypeScript 支持**: 完整的类型安全保障
- **响应式布局**: 适配不同屏幕尺寸的设备
- **状态管理**: 使用 Pinia 进行集中式状态管理
- **路由管理**: 使用 Vue Router 实现页面导航
- **样式系统**: 使用 Tailwind CSS 实现现代化 UI
- **API 通信**: 配置化的 API 接口调用

## 推荐 IDE 设置

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (并禁用 Vetur)。

## 推荐浏览器设置

- 基于 Chromium 的浏览器 (Chrome, Edge, Brave 等):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [在 Chrome DevTools 中开启自定义对象格式化程序](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [在 Firefox DevTools 中开启自定义对象格式化程序](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## TypeScript 支持

项目完全支持 TypeScript，包括 `.vue` 单文件组件的类型检查。我们使用 `vue-tsc` 进行类型检查，确保代码的类型安全。

## 自定义配置

请参阅 [Vite 配置参考](https://vite.dev/config/) 了解如何自定义构建配置。

## 项目设置

```sh
# 安装依赖
pnpm install
```

### 开发环境

```sh
# 启动开发服务器（带热重载）
pnpm dev
```

应用将在 `http://localhost:5173` 启动。

### 生产构建

```sh
# 类型检查 + 构建生产版本
pnpm build
```

构建产物将输出到 `dist` 目录。

### 测试

```sh
# 运行单元测试（Vitest）
pnpm test:unit

# 运行端到端测试（Playwright）
# 首次运行需要安装浏览器
npx playwright install

# 构建项目（CI 环境需要）
pnpm build

# 运行所有端到端测试
pnpm test:e2e

# 仅在 Chromium 浏览器上运行测试
pnpm test:e2e --project=chromium

# 运行特定测试文件
pnpm test:e2e tests/vue.spec.ts

# 调试模式运行测试
pnpm test:e2e --debug
```

### 代码质量

```sh
# 使用 ESLint 检查代码
pnpm lint
```

## 与后端的交互

前端应用通过 API 与后端服务通信。API 配置位于 `src/config/api.ts` 文件中。确保在开发前正确配置 API 端点。

## 部署

前端应用可以通过多种方式部署，包括静态文件服务器、Docker 容器等。完整的部署指南请参阅项目根目录下的 [部署文档](../Deployment/README.md)。

## 开发贡献

1. 确保安装了所有依赖
2. 遵循项目的代码风格和命名规范
3. 编写单元测试覆盖新功能
4. 提交代码前运行 lint 和测试

## 许可证

MIT License
