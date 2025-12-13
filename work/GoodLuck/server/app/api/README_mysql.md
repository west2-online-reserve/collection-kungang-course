

## 🚀 快速开始

### 1. 环境准备

确保已安装：
- Python 3.7+
- MySQL 5.7+ 或 MariaDB 10.0+

### 2. 安装依赖

```bash
pip install -r requirements_mysql.txt
```

### 3. 数据库配置

修改 `mysql.py` 第768行的数据库配置：

```python
config = DatabaseConfig(
    host='localhost',
    user='root',
    password='your_mysql_password',  # 修改为您的MySQL密码
    database='class_management'
)
```

### 4. 启动服务

```bash
# 方法1：使用启动脚本（推荐）
python run_mysql_api.py

# 方法2：直接运行
python app_mysql.py
```

服务将在 `http://localhost:5000` 启动

### 5. 测试API

```bash
python test_mysql_api.py
```

## 📡 API 接口文档

### 认证相关

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
    "username": "testuser",
    "password": "123456",
    "height": 175.5,
    "weight": 70.2
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "123456"
}
```

返回：
```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "username": "testuser",
            "height": 175.5,
            "weight": 70.2
        }
    }
}
```

#### 获取用户信息
```http
GET /api/auth/profile
Authorization: Bearer <token>
```

#### 更新用户信息
```http
PUT /api/auth/update-profile
Authorization: Bearer <token>
Content-Type: application/json

{
    "password": "new_password",
    "height": 180.0,
    "weight": 75.0
}
```

### 评分管理

#### 添加评分
```http
POST /api/ratings
Authorization: Bearer <token>
Content-Type: application/json

{
    "rating_content": "表现优秀，积极主动"
}
```

#### 获取所有评分
```http
GET /api/ratings
Authorization: Bearer <token>
```

#### 获取特定评分
```http
GET /api/ratings/{rating_id}
Authorization: Bearer <token>
```

### 历史记录

#### 获取用户历史记录
```http
GET /api/history
Authorization: Bearer <token>
```

#### 获取所有历史记录（管理员）
```http
GET /api/history/all
Authorization: Bearer <token>
```

### 登录记录

#### 获取用户登录记录
```http
GET /api/login-records
Authorization: Bearer <token>
```

#### 获取所有登录记录（管理员）
```http
GET /api/login-records/all
Authorization: Bearer <token>
```

### 管理员接口

#### 获取所有用户
```http
GET /api/admin/users
Authorization: Bearer <token>
```

#### 获取数据库信息
```http
GET /api/admin/database-info
Authorization: Bearer <token>
```

### 基础接口

#### 首页
```http
GET /
```

#### 健康检查
```http
GET /api/health
```

## 🗃️ 数据库结构

系统使用以下4个表：

### users（用户表）
- `id` - 用户ID（主键）
- `username` - 用户名（唯一）
- `password` - 密码（SHA256哈希）
- `height` - 身高
- `weight` - 体重

### login_records（登录记录表）
- `id` - 记录ID（主键）
- `user_id` - 用户ID（外键）
- `login_time` - 登录时间

### rating_scores（评分表）
- `rating_id` - 评分ID（主键）
- `rating_content` - 评分内容

### history_records（历史记录表）
- `record_id` - 记录ID（主键）
- `user_id` - 用户ID（外键）
- `rating_id` - 评分ID（外键）

## 🛠️ 项目结构

```
api/
├── mysql.py                 # 数据库管理类（核心）
├── app_mysql.py            # Flask应用主文件
├── config_mysql.py         # 配置文件
├── requirements_mysql.txt  # Python依赖
├── run_mysql_api.py        # 启动脚本
├── test_mysql_api.py       # 测试脚本
└── README_mysql.md         # 项目文档
```

## 🔧 配置说明

### 数据库配置
在 `mysql.py` 中修改：
```python
config = DatabaseConfig(
    host='localhost',           # MySQL服务器地址
    user='root',               # 用户名
    password='your_password',   # 密码
    database='class_management' # 数据库名
)
```

### JWT配置
在 `app_mysql.py` 中修改：
```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
```

## 🧪 测试

### 使用curl测试

```bash
# 1. 注册
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456",
    "height": 175.5,
    "weight": 70.2
  }'

# 2. 登录
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'

# 3. 获取用户信息（需要token）
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer <your-token>"
```

### 使用Python测试
```bash
python test_mysql_api.py
```

## 📋 运行方法

### 方法1：使用启动脚本（推荐）
```bash
python run_mysql_api.py
```

启动脚本会自动：
- 检查依赖是否安装
- 测试数据库连接
- 初始化数据库和表
- 启动Flask应用

### 方法2：直接运行
```bash
python app_mysql.py
```

### 方法3：使用Flask命令
```bash
set FLASK_APP=app_mysql.py
set FLASK_ENV=development
flask run
```

## ⚠️ 注意事项

1. **数据库配置**: 
   - 确保MySQL服务正在运行
   - 修改 `mysql.py` 中的数据库密码
   - 系统会自动创建数据库和表

2. **安全配置**:
   - 生产环境请修改 `SECRET_KEY` 和 `JWT_SECRET_KEY`
   - 密码使用SHA256哈希存储

3. **权限管理**:
   - 当前所有接口都需要JWT认证
   - 管理员接口需要额外的权限控制（可自行扩展）

4. **错误处理**:
   - 所有接口都有统一的错误响应格式
   - 详细的错误信息便于调试

## 🚀 部署建议

### 开发环境
- 使用内置的Flask开发服务器
- 开启DEBUG模式

### 生产环境
- 使用Gunicorn或uWSGI
- 配置Nginx反向代理
- 使用环境变量管理敏感配置
- 配置HTTPS

```bash
# 使用Gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_mysql:app
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License
