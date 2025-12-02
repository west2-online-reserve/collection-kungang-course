# 后端 API 文档

本文档概述了校园打卡系统后端可用的 API 端点。

## 基础 URL

所有 API 端点的前缀均为 `/api`。

## 认证 (Authentication)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | 注册新用户 | 否 |
| `POST` | `/login` | 登录并获取令牌 | 否 |

## 用户管理 (User Management)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `POST` | `/user/avatar/update` | 更新用户头像 URL | 是 |
| `POST` | `/user/avatar/upload` | 上传新头像图片 | 是 |
| `GET` | `/user/info` | 获取当前用户信息 | 是 |
| `POST` | `/user/password/change` | 修改用户密码 | 是 |
| `POST` | `/user/name/change` | 修改用户昵称 | 是 |

## 历史事件 (History Events)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `GET` | `/history/events` | 获取所有历史事件 | 否 |
| `GET` | `/history/event` | 根据 ID 获取单个历史事件 | 否 |
| `POST` | `/history/event/create` | 创建新的历史事件 | 否 |
| `POST` | `/history/event/update` | 更新现有的历史事件 | 否 |
| `POST` | `/history/event/delete` | 删除历史事件 | 否 |

## 时间轴 (Timelines)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `GET` | `/history/timelines` | 获取特定事件的时间轴 | 否 |
| `POST` | `/history/timeline/create` | 创建新的时间轴条目 | 否 |

## 校园打卡 (Campus Check-in)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `GET` | `/checkin/comments/{locationId}` | 获取地点的评论 | 是 |
| `GET` | `/checkin/danmaku/{locationId}` | 获取地点的弹幕 | 是 |
| `POST` | `/checkin/submit` | 提交打卡 | 是 |

## 学院互动 (College Interaction)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `GET` | `/college/comments/{collegeId}` | 获取学院的评论 | 是 |
| `POST` | `/college/comment` | 为学院发表评论 | 是 |
| `DELETE` | `/college/comment/{commentId}` | 删除评论 | 是 |
| `POST` | `/college/comment/{commentId}/like` | 对评论点赞/取消点赞 | 是 |

## 游戏 (合成大西瓜)

| 方法 | 端点 | 描述 | 需要认证 |
| :--- | :--- | :--- | :--- |
| `POST` | `/game/watermelon/score` | 提交游戏分数 | 是 |
| `GET` | `/game/watermelon/leaderboard` | 获取全球排行榜 | 否 |
| `GET` | `/game/watermelon/personal` | 获取个人最高分 | 是 |
