# AAQ 安装部署指南

## 系统要求

- **操作系统**: Windows 10+ / Linux / macOS
- **Python**: 3.10+
- **Node.js**: 16+ (前端开发)
- **内存**: 2GB+
- **磁盘**: 500MB+

## 后端安装

### 1. 克隆项目
```bash
git clone https://github.com/Sigebolo/MOLTBOY.git
cd Atom-Quant
```

### 2. 安装 Python 依赖
```bash
pip install -r requirements.txt
```

依赖清单：
| 包 | 用途 |
|----|------|
| akshare | A 股行情数据 |
| pandas / numpy | 数据处理 |
| fastapi / uvicorn | API 服务器 |
| httpx | HTTP 客户端 (测试) |
| statsmodels / scipy | 统计分析 |
| pyyaml | 配置文件 |
| requests | 网络请求 |
| pytest | 测试框架 |

### 3. 验证安装
```bash
python -m pytest tests/ -v
```
期望结果：106 tests passed

## 前端安装

```bash
cd src/dashboard
npm install
```

## 启动服务

### 方法 1: 使用批处理脚本 (推荐)
```bash
# 启动后端 API 服务器
.\run_aaq_dashboard_server.bat

# 在另一个终端启动前端
cd src/dashboard && npm run dev
```

### 方法 2: 手动启动
```bash
# 后端 (端口 8001)
uvicorn src.server:app --host 0.0.0.0 --port 8001

# 前端 (端口 5173)
cd src/dashboard && npm run dev
```

### 方法 3: 使用部署脚本
```bash
python deploy.py           # 完整部署
python deploy.py --check-only  # 仅预检
```

## 访问地址

| 服务 | URL |
|------|-----|
| Dashboard | http://localhost:5173 |
| API Server | http://localhost:8001 |
| API 健康检查 | http://localhost:8001/ |

## 配置文件

主配置: `config.yaml`

```yaml
backend:
  host: "0.0.0.0"
  port: 8001
  log_level: "INFO"
  workers: 4

frontend:
  build_dir: "src/dashboard/dist"
  port: 5173

data:
  portfolio_path: "data/portfolio.json"
  backtest_path: "data/backtest_results.json"
  log_dir: "logs"
  retention_days: 30

risk:
  max_position_pct: 0.20
  safety_buffer_trigger_price: 100.0
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 端口 8001 被占用 | `netstat -ano | findstr 8001` 然后 `taskkill /PID <pid> /F` |
| AkShare 数据获取失败 | 检查网络连接，确认 pip 版本最新 |
| 前端白屏 | 确认后端已启动，检查 `vite.config.js` proxy 设置 |
| pytest 导入错误 | 从项目根目录运行，确认 `src/__init__.py` 存在 |
