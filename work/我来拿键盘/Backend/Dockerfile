# 使用golang官方镜像作为构建环境
FROM golang:1.24-alpine AS builder

# 设置工作目录
WORKDIR /app

# 安装必要的构建工具
RUN apk add --no-cache git

# 复制依赖文件并下载依赖
COPY go.mod go.sum ./
RUN go mod download

# 复制所有源代码
COPY . .

# 构建应用程序
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o backend main.go

# 使用轻量级的alpine作为运行环境
FROM alpine:latest

# 设置工作目录
WORKDIR /app

# 安装运行时依赖
RUN apk --no-cache add ca-certificates tzdata

# 设置时区为上海
ENV TZ=Asia/Shanghai

# 从构建阶段复制可执行文件
COPY --from=builder /app/backend /app/

# 创建静态资源目录
RUN mkdir -p /app/static/avatar /app/static/checkin

# 从构建阶段复制静态资源
COPY --from=builder /app/static/ /app/static/

# 设置环境变量
ENV GIN_MODE=release

# 暴露端口
EXPOSE 8080

# 运行应用程序
CMD ["./backend"]