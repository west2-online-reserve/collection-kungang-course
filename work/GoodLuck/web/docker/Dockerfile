# 构建阶段
FROM node:24-alpine AS builder

WORKDIR /app

# 复制包文件并安装依赖
COPY web/package*.json ./
RUN npm install

# 复制源代码并构建
COPY web/ .
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建好的静态文件到 Nginx
COPY --from=builder app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]