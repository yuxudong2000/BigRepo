# 强基2026 内网部署指南

## 项目概述
这是一个静态网站项目（2026强基计划招生汇总），部署到内网域名 `qiangji2026.frontend-cloud.corp.kuaishou.com`。

## jokecommic/qiangji2026 - 2026强基计划招生汇总

### 项目信息
- **项目 ID**：qiangji2026
- **内网域名**：https://qiangji2026.frontend-cloud.corp.kuaishou.com
- **部署 ID**：532

### 静态文件
- `index.html`（136 KB，主页面）

### 快速部署

此项目为纯静态站点（仅含 `index.html`），可通过以下方式部署到内网：

#### 方式一：使用内网静态站点托管平台重新上传
登录内网前端托管平台，找到项目 `qiangji2026`（ID: 532），重新上传 `index.html` 即可。

#### 方式二：本地起临时 HTTP 服务器预览

```bash
cd jokecommic/qiangji2026
python3 -m http.server 8080
```

**启动后访问**：http://localhost:8080

```yaml
subProjectPath: jokecommic/qiangji2026
command: python3 -m http.server 8080
cwd: jokecommic/qiangji2026
port: 8080
previewUrl: http://localhost:8080
description: 2026强基计划招生汇总静态网站，内网部署目标域名 qiangji2026.frontend-cloud.corp.kuaishou.com
deployConfig: .static-site-deploy.json
```
