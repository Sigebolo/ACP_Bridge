# AAQ API 接口文档

**Base URL**: `http://localhost:8001`

## 端点列表

### GET /
健康检查

**Response**:
```json
{
  "status": "AAQ Server Running",
  "time": "2026-02-22T21:30:00.000000"
}
```

---

### GET /api/portfolio
获取当前持仓

**Response**:
```json
{
  "holdings": [
    {
      "symbol": "110088",
      "name": "淮22",
      "cost": 115.0,
      "qty": 10
    }
  ]
}
```

---

### GET /api/bonds
获取双低策略候选 (Pancake Candidates)

**Response**:
```json
{
  "candidates": [
    {
      "bond_code": "127045",
      "bond_name": "中矿转债",
      "price": 98.5,
      "premium": 8.2,
      "double_low_score": 106.7,
      "credit_rating": "AA",
      "ytm": 2.5
    }
  ],
  "count": 15
}
```

**说明**: 数据来源 `data/pancake_candidates.json`。NaN/Infinity 值自动转为 null。

---

### GET /api/alerts
获取最新风险告警

**Response**:
```json
{
  "active_alerts": [
    {
      "title": "安全缓冲",
      "details": "110088 安全缓冲触发 价格<100",
      "level": "CRITICAL",
      "timestamp": "21:30"
    }
  ]
}
```

**说明**: 从最新 `data/AAQ_Report_*.md` 解析。Level: `CRITICAL` 或 `INFO`。

---

### GET /api/market
获取市场状态

**Response**:
```json
{
  "safety_score": 85,
  "market_sentiment": "Neutral",
  "last_updated": "2026-02-22T21:30:00.000000"
}
```

**说明**: 当前为静态模拟值，v2.0 将接入实时计算。

---

### GET /api/backtest
获取回测结果 (权益曲线和交易记录)

**Response**:
```json
{
  "strategy_name": "A-Share Tail Strategy",
  "backtest_period": "2023-01-01 to 2024-01-01",
  "initial_capital": 100000.0,
  "final_capital": 102500.0,
  "total_return": 0.025,
  "total_trades": 12,
  "performance_metrics": {
    "win_rate": 58.33,
    "sharpe_ratio": 0.85,
    "max_drawdown": -3.21
  },
  "equity_curve": [
    {"date": "2023-01-03", "equity": 100000.0}
  ],
  "trades": [
    {
      "symbol": "000001",
      "entry_date": "2023-02-15",
      "exit_date": "2023-03-01",
      "entry_price": 15.2,
      "exit_price": 16.8,
      "pnl_pct": 10.52,
      "exit_reason": "Take Profit"
    }
  ]
}
```

## 错误处理

所有端点在异常时返回：
```json
{
  "holdings": [],
  "error": "错误信息"
}
```

## CORS 配置

当前允许所有来源 (`*`)。生产环境应限制为：
```
http://localhost:5173
```
