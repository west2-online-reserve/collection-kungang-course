# Cloudflare Tunnel 设置

本目录包含使用 Cloudflare Tunnel 将本地服务暴露到互联网的配置。

## 先决条件

- 已安装 `cloudflared` CLI 工具。
- 一个 Cloudflare 账户和一个已配置的域名。

## 配置

`config.yml` 文件定义了隧道配置：

```yaml
tunnel: my-computer
credentials-file: .\my-computer.json
protocol: auto
ingress:
  - hostname: fzu-hi-museum.zviolin.online
    service: http://localhost:80
  - hostname: api.fzu-hi-museum.zviolin.online
    service: http://localhost:8080
  - service: http_status:404
```

- **`fzu-hi-museum.zviolin.online`**: 路由到前端 (`localhost:80`)。
- **`api.fzu-hi-museum.zviolin.online`**: 路由到后端 (`localhost:8080`)。

## 运行 Tunnel

要启动隧道，请在此目录中运行以下命令：

```bash
cloudflared tunnel --config=.\config.yml run my-computer
```

请确保 `my-computer.json`（凭证文件）存在，并在 `config.yml` 中正确引用。