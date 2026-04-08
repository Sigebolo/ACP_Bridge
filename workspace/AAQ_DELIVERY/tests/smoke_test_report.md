# AAQ 冒烟测试报告

**日期**: 2026-02-22
**执行人**: Antigravity (QA)
**环境**: Windows / Python 3.11.9 / pytest 9.0.1

---

## 测试概要

| 项目 | 结果 |
|------|------|
| 总测试数 | 106 |
| 通过 | 106 (100%) |
| 失败 | 0 |
| 警告 | 0 |
| 执行时间 | 104.14s |

## 模块测试明细

| 测试文件 | 用例数 | 状态 |
|----------|--------|------|
| test_advanced_cointegration.py | 6 | ✅ ALL PASS |
| test_api_integration.py | 6 | ✅ ALL PASS |
| test_backtest_v3.py | 3 | ✅ ALL PASS |
| test_cointegration.py | 7 | ✅ ALL PASS |
| test_fund_agent.py | 18 | ✅ ALL PASS |
| test_fund_data.py | 8 | ✅ ALL PASS |
| test_fund_screener.py | 7 | ✅ ALL PASS |
| test_integration_workflow.py | 5 | ✅ ALL PASS |
| test_pancake_suite.py | 5 | ✅ ALL PASS |
| test_reporter.py | 1 | ✅ ALL PASS |
| test_risk_engine.py | 1 | ✅ ALL PASS |
| test_risk_engine_comprehensive.py | 5 | ✅ ALL PASS |
| test_risk_system.py | 6 | ✅ ALL PASS |
| test_scanner.py | 3 | ✅ ALL PASS |
| test_scanner_comprehensive.py | 5 | ✅ ALL PASS |
| test_scanner_v3.py | 3 | ✅ ALL PASS |
| test_simple_advanced.py | 5 | ✅ ALL PASS |

**合计**: 106 tests / 17 test files

## 关键模块验证

### 1. 交易逻辑 (Pancake Strategy)
- 安全垫过滤 ✅
- 到期日过滤 ✅
- 均线弱势/击穿检测 ✅
- 紧急止损 ✅

### 2. 风控引擎 (Risk Engine)
- 安全缓冲计算 ✅
- 双低检测 ✅
- 止损计算 ✅
- 风险评分矩阵 ✅
- 告警生成与优先级 ✅

### 3. API 集成 (FastAPI Server)
- /api/bonds 端点 ✅
- /api/portfolio 端点 ✅
- /api/alerts 端点 ✅
- /api/backtest 端点 ✅
- /api/market (健康检查) ✅
- 数据流式更新 ✅

### 4. 回测引擎 (Backtest Engine)
- 数据获取 (AkShare) ✅
- 尾部信号计算 ✅
- 策略执行 ✅

### 5. 部署脚本
- `deploy.py --check-only` 预检通过 ✅
- 目录验证通过 ✅
- Python 版本检查通过 ✅

## 已修复问题
- pandas `SettingWithCopyWarning` in `backtest_engine.py` — 已修复 (commit 4493ed8)

## 结论
**✅ 冒烟测试全部通过，系统可安全上线。**
