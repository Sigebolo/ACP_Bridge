# AAQ 用户操作指南

## 日常操作

### 1. 市场扫描 (每日执行)

运行全量审计扫描：
```bash
.\aaq_full_audit.bat
```

扫描结果保存在 `data/AAQ_Report_YYYY-MM-DD.md`。

### 2. A 股尾部信号扫描

```bash
.\aaq_run_scanner.bat
# 或手动运行
python src/vibe_scanner_v3.py
```

扫描前 30 只活跃股票的尾部异动信号，结果保存到 `data/signals.json`。

### 3. 回测策略

```bash
python debug_backtest.py
# 或使用回测引擎
python src/backtest_engine.py
```

回测结果保存到 `data/backtest_results.json`，可在 Dashboard 的 Backtester 标签查看。

### 4. 查看 Dashboard

启动服务后访问 http://localhost:5173，包含以下标签：
- **Bonds** — 双低/Pancake 候选列表
- **Portfolio** — 当前持仓
- **Alerts** — 风险告警
- **Backtester** — 回测结果图表

### 5. 管理持仓

```bash
# 添加
python src/portfolio_manager.py add --symbol 110088 --name "淮22" --cost 115 --qty 10

# 查看
python src/portfolio_manager.py list

# 删除
python src/portfolio_manager.py remove --symbol 110088
```

### 6. 可转债策略测试 (Pancake)

```bash
.\aaq_test_pancake.bat
```

### 7. Git 备份

```bash
.\aaq_commit.bat
```

## 数据文件说明

| 文件 | 说明 | 更新频率 |
|------|------|----------|
| `data/portfolio.json` | 当前持仓 | 手动更新 |
| `data/pancake_candidates.json` | 双低候选 | 每次扫描 |
| `data/backtest_results.json` | 回测结果 | 每次回测 |
| `data/signals.json` | 尾部信号 | 每次扫描 |
| `data/AAQ_Report_*.md` | 日报 | 每日审计 |
| `logs/` | 运行日志 | 自动 |

## 注意事项

1. **数据源**: 当前主要使用 AkShare，Jisilu 需要登录 Cookie（v2.0 支持）
2. **端口**: API 默认 8001，Dashboard 默认 5173
3. **时区**: 系统使用本地时区，交易数据为 UTC+8
4. **日志**: 保留 30 天，超时自动清理
