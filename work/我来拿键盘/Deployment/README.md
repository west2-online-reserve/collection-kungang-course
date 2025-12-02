# 部署指南

本目录包含使用 Docker Compose 部署校园打卡系统所需的配置文件。

## 先决条件

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 服务

`docker-compose.yml` 文件定义了以下服务：

- **`db`**: MySQL 8.0 数据库。
- **`redis`**: Redis 7 (Alpine) 缓存服务。
- **`backend`**: Go 后端应用程序。
- **`frontend`**: Vue.js 前端应用程序（取决于 Dockerfile，通常通过 Nginx 等服务）。

## 开始使用

1.  **进入 Deployment 目录：**

    ```bash
    cd Deployment
    ```

2.  **启动服务：**

    ```bash
    docker-compose up -d
    ```

    此命令将构建镜像（如果需要）并以分离模式启动容器。

3.  **验证部署：**

    - **前端**: 访问 `http://localhost:80`（或 `docker-compose.yml` 中映射的端口）。
    - **后端 API**: 访问 `http://localhost:8080`。
    - **数据库**: 端口 `3307` 映射到容器的 `3306`。

## 环境变量

您可以在 `docker-compose.yml` 文件或 `.env` 文件中配置以下环境变量：

- `DB_PASSWORD`: MySQL 的 root 密码（默认：`123456`）。
- `DB_NAME`: 数据库名称（默认：`fzu_history`）。
- `JWT_SECRET`: JWT 认证的密钥。

## Cloudflare Tunnel

如需安全地将应用程序暴露到互联网，请参阅 [Cloudflare 文档](./cloudflare/README.md)。
