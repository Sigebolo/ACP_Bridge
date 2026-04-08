# Atom Alpha Quant (AAQ)

AAQ 是一套面向 **A 股可转债** 的自动化量化交易与监控系统，聚焦安全垫策略（双低/Pancake）和风险穿透分析。

## 功能特性

- **市场扫描** — 实时轮询 AkShare 数据，过滤双低候选
- **尾部信号** — A 股尾部异动检测与预警
- **风控引擎** — 安全缓冲、均线击穿、紧急止损
- **回测系统** — 历史数据回测与绩效分析
- **Dashboard** — Vue 3 前端实时展示
- **基金研究** — 基金筛选与分析代理
- **协整分析** — Johansen 多资产协整 + OU 过程

## 技术栈

| 层 | 技术 |
|----|------|
| Backend | Python 3.11 + FastAPI + Uvicorn |
| Frontend | Vue 3 + Vite + Chart.js |
| 数据源 | AkShare (行情) + Jisilu (信用/公告) |
| 存储 | JSON 文件持久化 (`data/`) |
| 测试 | pytest (106 test cases) |

## 快速开始

请参阅 [INSTALL.md](INSTALL.md) 了解安装步骤。

## 文档索引

| 文档 | 说明 |
|------|------|
| [INSTALL.md](INSTALL.md) | 安装部署指南 |
| [USER_GUIDE.md](USER_GUIDE.md) | 用户操作指南 |
| [API_REFERENCE.md](API_REFERENCE.md) | API 接口文档 |
| [STRATEGY_LOGIC.md](STRATEGY_LOGIC.md) | 策略逻辑说明 |

## 版本信息

- **当前版本**: v1.0 Production Ready
- **最后更新**: 2026-02-22
