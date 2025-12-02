
FROM node:20-alpine AS builder

WORKDIR /app

# 安装 pnpm
RUN npm install -g pnpm

# 安装依赖
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# 构建
COPY . .
RUN pnpm run build

# 使用本地已有 nginx:alpine
FROM nginx:alpine

# 安装 envsubst 工具（用于环境变量替换）
RUN apk add --no-cache gettext

# 静态文件复制到 nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# 自定义 nginx 配置
COPY ./nginx.conf /etc/nginx/conf.d/default.conf.template

# 创建启动脚本
COPY <<'EOF' /docker-entrypoint.d/10-envsubst-on-templates.sh
#!/bin/sh

# 替换 Nginx 配置中的环境变量
envsubst '${SERVER_NAME},${BACKEND_API_URL},${BACKEND_STATIC_URL},${NGINX_WORKER_PROCESSES},${NGINX_WORKER_CONNECTIONS},${NGINX_LOG_LEVEL},${STATIC_CACHE_TIME}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# 确保脚本可执行
chmod +x /docker-entrypoint.d/10-envsubst-on-templates.sh
EOF

# 确保启动脚本可执行
RUN chmod +x /docker-entrypoint.d/10-envsubst-on-templates.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
