# 华为云 openGauss 数据库配置指南

## 一、获取数据库连接信息

### 1. 登录华为云控制台
访问 https://console.huaweicloud.com/

### 2. 进入 GaussDB(for openGauss) 服务
- 在控制台搜索 "GaussDB" 或 "openGauss"
- 进入数据库实例列表

### 3. 查看实例详情
点击您的数据库实例，获取以下信息：
- **内网IP地址**: 用于同一VPC内的服务器连接
- **公网IP地址**: 用于外网访问（需要先绑定弹性公网IP）
- **端口号**: 通常是 8000
- **数据库用户名**: 创建实例时设置的用户名
- **数据库密码**: 创建实例时设置的密码

## 二、配置安全组规则

### 1. 进入安全组设置
在数据库实例详情页面，找到"安全组"选项

### 2. 添加入方向规则
- 协议: TCP
- 端口: 8000（或您的数据库端口）
- 源地址: 
  - 如果是本地开发: 添加您的公网IP/32
  - 如果是服务器: 添加服务器的IP/32
  - 测试环境可临时使用 0.0.0.0/0（不推荐生产环境）

### 3. 保存规则
确保规则已生效

## 三、配置项目

### 1. 编辑 backend/config.py

```python
DB_CONFIG = {
    'host': '123.456.789.012',           # 替换为您的华为云数据库IP
    'port': 8000,                         # 确认端口号
    'database': 'stray_animal_db',        # 数据库名称
    'user': 'gaussdb_user',               # 替换为您的用户名
    'password': 'YourPassword123!',       # 替换为您的密码
    'sslmode': 'disable'                  # 如需SSL，改为 'require'
}

SECRET_KEY = 'your-random-secret-key-here'  # 生成一个随机密钥
```

### 2. 测试连接

```bash
cd backend
python test_connection.py
```

如果连接成功，会显示数据库版本信息。

### 3. 初始化数据库

```bash
python init_database.py
```

## 四、常见问题排查

### 问题1: 连接超时
**原因**: 安全组规则未正确配置
**解决**: 
- 检查安全组是否允许您的IP访问
- 确认使用的是正确的IP地址（公网/内网）

### 问题2: 认证失败
**原因**: 用户名或密码错误
**解决**: 
- 在华为云控制台重置数据库密码
- 确认用户名拼写正确

### 问题3: 数据库不存在
**原因**: 首次连接，数据库未创建
**解决**: 
- 运行 `python init_database.py` 会自动创建数据库

### 问题4: SSL 连接错误
**原因**: SSL 配置不匹配
**解决**: 
- 在 config.py 中设置 `'sslmode': 'disable'`
- 或下载华为云提供的SSL证书并配置

## 五、安全建议

### 1. 生产环境配置
- ✓ 使用强密码
- ✓ 限制安全组只允许特定IP访问
- ✓ 启用SSL连接
- ✓ 定期备份数据库
- ✓ 修改默认管理员密码

### 2. 网络配置
- 优先使用内网连接（更快更安全）
- 公网连接仅用于开发测试
- 生产环境建议使用VPN或专线

### 3. 密钥管理
- 不要将 config.py 提交到版本控制
- 使用环境变量存储敏感信息
- 定期更换密钥

## 六、使用环境变量（推荐）

### 1. 修改 config.py 支持环境变量

```python
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 8000)),
    'database': os.getenv('DB_NAME', 'stray_animal_db'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_password')
}

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
```

### 2. 设置环境变量

**Linux/Mac:**
```bash
export DB_HOST=123.456.789.012
export DB_PORT=8000
export DB_NAME=stray_animal_db
export DB_USER=gaussdb_user
export DB_PASSWORD=YourPassword123!
export SECRET_KEY=your-random-secret-key
```

**Windows:**
```cmd
set DB_HOST=123.456.789.012
set DB_PORT=8000
set DB_NAME=stray_animal_db
set DB_USER=gaussdb_user
set DB_PASSWORD=YourPassword123!
set SECRET_KEY=your-random-secret-key
```

## 七、连接示例

### 使用 gsql 客户端连接

```bash
# 安装 gsql 客户端（如果还没有）
# 从华为云官网下载 openGauss 客户端工具

# 连接到数据库
gsql -h 123.456.789.012 -p 8000 -U gaussdb_user -W YourPassword123! -d postgres

# 查看数据库列表
\l

# 切换到项目数据库
\c stray_animal_db

# 查看表
\dt
```

## 八、备份与恢复

### 备份数据库
```bash
gs_dump -h 123.456.789.012 -p 8000 -U gaussdb_user -W YourPassword123! -d stray_animal_db -f backup.sql
```

### 恢复数据库
```bash
gsql -h 123.456.789.012 -p 8000 -U gaussdb_user -W YourPassword123! -d stray_animal_db -f backup.sql
```

## 九、性能优化建议

1. **连接池配置**: 在生产环境使用连接池（如 psycopg2.pool）
2. **索引优化**: 已在初始化脚本中创建必要索引
3. **查询优化**: 使用 EXPLAIN 分析慢查询
4. **定期维护**: 定期执行 VACUUM 和 ANALYZE

## 十、监控与日志

### 华为云控制台监控
- CPU使用率
- 内存使用率
- 磁盘使用率
- 连接数
- QPS（每秒查询数）

### 应用日志
在 app.py 中添加日志记录：
```python
import logging
logging.basicConfig(level=logging.INFO)
```

---

如有问题，请参考华为云 openGauss 官方文档：
https://support.huaweicloud.com/gaussdb_opengauss/
