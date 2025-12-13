# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
# 先备份并替换默认软件源
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list.d/debian.sources
# 然后更新并安装软件包
RUN apt-get update && apt-get install -y gcc libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY ./app/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .


# 暴露端口
EXPOSE 5000

# 启动命令

CMD ["celery", "-A", "app.celery_app", "worker", "--loglevel=info", "--concurrency=4"]