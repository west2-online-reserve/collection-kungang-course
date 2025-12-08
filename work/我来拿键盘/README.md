# 校园打卡系统

欢迎来到校园打卡系统项目！这是一个基于 Web 的互动应用程序，旨在让用户探索校园历史、在特定地点打卡互动，并参与趣味游戏。

## 项目概述

校园打卡系统是一个集成了用户认证、历史探索、地理位置打卡、学院互动和休闲游戏的综合性平台。通过这个系统，用户可以深入了解校园文化，与其他用户进行互动，并在游戏中获得乐趣。

## 项目结构

项目采用前后端分离架构，组织在以下目录中：

- **`Backend`**: 使用 Go 构建的服务器端应用程序。它处理 API 请求、数据库交互 (MySQL) 和缓存 (Redis)。
- **`Frontend`**: 使用 Vue 3 + TypeScript + Vite 构建的客户端应用程序。它为系统提供现代化、响应式的用户界面。
- **`Deployment`**: 包含使用 Docker Compose 和 Cloudflare Tunnels 部署应用程序的完整配置文件。
- **`Data`**: 数据库初始化脚本，用于创建表结构和初始数据。

## 快速开始

要快速启动并运行系统，请参阅 [部署文档](./Deployment/README.md)。

## 核心功能

### 用户认证与管理
- 用户注册、登录功能
- 个人资料管理（头像、密码、昵称修改）
- JWT 令牌认证机制

### 历史探索
- 历史事件浏览与时间轴展示
- 历史博物馆页面，详细展示校园文化
- 按时间和主题分类的历史内容

### 校园打卡
- 地理位置打卡功能
- 打卡地点详情查看
- 用户评论和弹幕互动
- 打卡记录管理

### 学院互动
- 学院介绍与详情展示
- 学院相关帖子评论和点赞
- 学院间互动交流

### 休闲游戏
- "合成大西瓜" 游戏实现
- 游戏排行榜功能
- 游戏历史记录查看

## 技术栈

### 后端
- **语言**: Go 1.20+
- **Web 框架**: Gin
- **数据库**: MySQL
- **缓存**: Redis
- **认证**: JWT

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **编程语言**: TypeScript
- **UI 框架**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router
- **测试**: Vitest + Playwright

## 视频演示

以下是校园打卡系统的功能演示视频：

<video  controls>
  <source src="https://github.com/164321595/collection-kungang-course/releases/download/video-v1/ShowVideo.mp4" type="video/mp4">
  您的浏览器不支持 HTML5 视频标签。
</video>

或者您可以直接下载视频文件：[ShowVideo.mp4](https://github.com/164321595/collection-kungang-course/releases/download/video-v1/ShowVideo.mp4)

## 文档

- [后端 API 文档](./Backend/API.md)
- [前端文档](./Frontend/README.md)
- [部署指南](./Deployment/README.md)

## 开发与贡献

### 后端开发
请参阅后端目录中的文档和代码结构。

### 前端开发
请参阅前端目录中的 [README](./Frontend/README.md) 了解更多开发信息。

## 许可证

MIT License