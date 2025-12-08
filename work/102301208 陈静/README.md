# 福州大学流浪动物全生命周期管理平台

## 项目简介

本项目是一个基于 Vue 3 + Flask + openGauss 的福州大学流浪动物管理系统，实现了从发现、建档、投喂、医疗到领养的全生命周期数字化管理。

## 技术栈

### 前端
- Vue 3 + Vite
- Element Plus (UI组件库)
- Pinia (状态管理)
- Vue Router (路由管理)
- Axios (HTTP请求)
- ECharts (数据可视化)

### 后端
- Python Flask
- psycopg2-binary (openGauss数据库驱动)
- PyJWT (JWT认证)
- Flask-CORS (跨域支持)

### 数据库
- Huawei openGauss

## 功能模块

1. **用户与权限模块**
   - 用户注册/登录
   - 基于角色的访问控制 (RBAC)
   - 三种角色：普通用户、志愿者、管理员

2. **动物档案中心**
   - 动物信息管理（增删改查）
   - 多维度筛选（区域、状态、绝育情况）
   - 动物详情查看

3. **运维与关怀模块**
   - 日常投喂记录
   - 医疗健康日志
   - 经费统计

4. **领养审批工作流**
   - 在线申请领养
   - 管理员审批
   - 状态自动更新

5. **数据驾驶舱**
   - 绝育率统计（饼图）
   - 区域分布（柱状图）
   - 月度支出趋势（折线图）
   - 动物累计花费排行

## 安装与运行

### 1. 数据库初始化（华为云 openGauss）

#### 方式一：使用 gsql 客户端（推荐）

```bash
# 使用 gsql 连接到华为云 openGauss 数据库
gsql -h <华为云数据库IP> -p <端口> -U <用户名> -W <密码> -d postgres

# 在 gsql 中执行初始化脚本
\i backend/init_db.sql

# 或者直接执行
gsql -h <华为云数据库IP> -p <端口> -U <用户名> -W <密码> -d postgres -f backend/init_db.sql
```

#### 方式二：使用 Python 脚本初始化

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库连接信息
# 编辑 config.py 文件，填入华为云 openGauss 连接信息

CREATE USER gaussdb IDENTIFIED BY 'BigData@2025' SYSADMIN;

# 运行初始化脚本
python init_database.py
```

### 2. 配置后端数据库连接

创建 `backend/config.py` 文件：

```python
# 华为云 openGauss 数据库配置
DB_CONFIG = {
    'host': 'your-huawei-cloud-ip',      # 华为云数据库公网IP或内网IP
    'port': 8000,                         # openGauss 默认端口通常是 8000
    'database': 'stray_animal_db',
    'user': 'your_username',              # 数据库用户名
    'password': 'your_password'           # 数据库密码
}

# Flask 配置
SECRET_KEY = 'your-secret-key-change-in-production'
```

### 3. 后端启动

```bash
cd backend

# 启动后端服务
python app.py
```

后端将运行在 http://localhost:5000

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:3000

## 默认账号

- 用户名: admin
- 密码: admin123
- 角色: 管理员

## 项目结构

```
code/
├── backend/
│   ├── app.py              # Flask 主应用
│   ├── init_db.sql         # 数据库初始化脚本
│   └── requirements.txt    # Python 依赖
│
└── frontend/
    ├── src/
    │   ├── views/          # 页面组件
    │   │   ├── Login.vue
    │   │   ├── Register.vue
    │   │   ├── Animals.vue
    │   │   ├── AnimalDetail.vue
    │   │   ├── FeedRecords.vue
    │   │   ├── HealthLogs.vue
    │   │   ├── Adoptions.vue
    │   │   └── Dashboard.vue
    │   ├── layouts/        # 布局组件
    │   │   └── MainLayout.vue
    │   ├── stores/         # Pinia 状态管理
    │   │   └── auth.js
    │   ├── utils/          # 工具函数
    │   │   └── axios.js
    │   ├── router/         # 路由配置
    │   │   └── index.js
    │   ├── App.vue         # 根组件
    │   └── main.js         # 入口文件
    ├── index.html
    ├── package.json
    └── vite.config.js

## API 接口文档

### 认证接口
- POST /api/register - 用户注册
- POST /api/login - 用户登录

### 动物管理
- GET /api/animals - 获取动物列表
- GET /api/animals/:id - 获取动物详情
- POST /api/animals - 创建动物档案
- PUT /api/animals/:id - 更新动物信息
- DELETE /api/animals/:id - 删除动物

### 投喂记录
- GET /api/feed-records - 获取投喂记录
- POST /api/feed-records - 创建投喂记录

### 医疗记录
- GET /api/health-logs - 获取医疗记录
- POST /api/health-logs - 创建医疗记录

### 领养申请
- GET /api/adoptions - 获取领养申请
- POST /api/adoptions - 提交领养申请
- PUT /api/adoptions/:id/approve - 审批领养申请

### 统计数据
- GET /api/statistics/sterilization - 绝育率统计
- GET /api/statistics/zone-distribution - 区域分布
- GET /api/statistics/monthly-costs - 月度支出
- GET /api/statistics/animal-costs - 动物累计花费

## 数据库设计

### users (用户表)
- user_id (主键)
- username (用户名)
- password_hash (密码哈希)
- role (角色)
- contact (联系方式)

### animals (动物档案表)
- animal_id (主键)
- name (昵称)
- species (物种)
- zone (区域)
- status (状态)
- is_sterilized (是否绝育)
- photo_url (照片路径)

### feed_records (投喂记录表)
- record_id (主键)
- user_id (外键 -> users)
- animal_id (外键 -> animals)
- feed_time (投喂时间)
- food_content (食物内容)

### health_logs (医疗记录表)
- log_id (主键)
- animal_id (外键 -> animals)
- action_type (行为类型)
- cost (费用)
- log_date (日期)
- description (描述)

### adoption_applications (领养申请表)
- application_id (主键)
- user_id (外键 -> users)
- animal_id (外键 -> animals)
- status (状态)
- apply_reason (申请理由)
- create_time (创建时间)

## 华为云 openGauss 配置

详细的华为云数据库配置步骤请参考：[华为云openGauss配置指南.md](./华为云openGauss配置指南.md)

### 快速配置步骤

1. **获取华为云数据库连接信息**
   - 登录华为云控制台
   - 查看 GaussDB(for openGauss) 实例详情
   - 记录 IP、端口、用户名、密码

2. **配置安全组**
   - 添加入方向规则，开放数据库端口（通常是 8000）
   - 允许您的服务器IP访问

3. **测试连接**
   ```bash
   cd backend
   python test_connection.py
   ```

4. **初始化数据库**
   ```bash
   # 首次初始化
   python init_database.py
   
   # 如果需要重置数据库（删除旧数据）
   python reset_database.py
   
   # 查看数据库当前状态
   python 查看数据库状态.py
   ```

## GitHub 代码管理

### 首次上传代码到 GitHub

```bash
# 1. 初始化 Git 仓库（如果还没有初始化）
git init

# 2. 添加远程仓库
git remote add origin https://github.com/NICECJ/Campus-Stray-Animal-Lifecycle-Management-Platform.git

# 3. 添加所有文件到暂存区
git add .

# 4. 提交代码
git commit -m "Initial commit: 福州大学流浪动物全生命周期管理平台"

# 5. 推送到 GitHub（首次推送）
git push -u origin main
```
### 日常更新代码到 GitHub

```bash
# 1. 查看修改的文件
git status

# 2. 添加修改的文件到暂存区
git add .

# 3. 提交修改（填写有意义的提交信息）
git commit -m "描述你的修改内容"

# 4. 推送到 GitHub
git push origin main
```

### 常用 Git 命令

```bash
# 查看提交历史
git log

# 查看远程仓库信息
git remote -v

# 拉取最新代码
git pull origin main

# 创建新分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature

# 查看分支
git branch -a
```

### .gitignore 配置

确保项目根目录有 `.gitignore` 文件，避免上传敏感信息和不必要的文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/

# 配置文件（包含敏感信息）
backend/config.py

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# 构建输出
dist/
build/
*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db

# 日志文件
*.log

# 环境变量
.env
.env.local
```

### 提交信息规范

建议使用以下格式编写提交信息：

- `feat: 添加新功能` - 新功能
- `fix: 修复bug` - 修复问题
- `docs: 更新文档` - 文档更新
- `style: 代码格式调整` - 代码格式（不影响功能）
- `refactor: 代码重构` - 重构代码
- `perf: 性能优化` - 性能优化
- `test: 添加测试` - 测试相关
- `chore: 构建/工具变动` - 构建工具或辅助工具的变动

示例：
```bash
git commit -m "feat: 添加动物相册功能"
git commit -m "fix: 修复医疗记录时间格式显示问题"
git commit -m "docs: 更新README安装说明"
```

## 注意事项

1. 请确保华为云 openGauss 数据库实例正常运行
2. 配置 `backend/config.py` 中的数据库连接信息
3. 确保安全组规则允许访问数据库端口
4. 生产环境请修改 Flask 的 SECRET_KEY
5. 建议使用 HTTPS 协议保护用户数据安全
6. **重要：不要将 config.py 提交到 GitHub（已在 .gitignore 中配置）**
7. 上传代码前请检查是否包含敏感信息（密码、密钥等）
