# AAQ 部署检查清单

**项目**: Atom Alpha Quant (AAQ) v1.0
**日期**: 2026-02-22

## 部署前检查

### 环境
- [x] Python 3.10+ 已安装
- [x] Node.js 16+ 已安装 (前端)
- [x] 所有 pip 依赖已安装 (`requirements.txt`)
- [x] 前端依赖已安装 (`npm install`)

### 代码质量
- [x] 106/106 测试通过
- [x] 0 failures, 0 warnings
- [x] `SettingWithCopyWarning` 已修复
- [x] `deploy.py --check-only` 预检通过

### 数据
- [x] `data/` 目录存在
- [x] `data/portfolio.json` 存在 (可空数组)
- [x] `logs/` 目录存在

### 配置
- [x] `config.yaml` 存在且格式正确
- [x] API 端口 8001 未被占用
- [x] CORS 已配置

### Git
- [x] 所有代码已提交 (commit `4493ed8`)
- [x] 已推送至远程仓库
- [x] `.gitignore` 已更新

## 部署步骤

1. [ ] 执行 `python deploy.py --check-only` 确认环境
2. [ ] 启动后端: `uvicorn src.server:app --host 0.0.0.0 --port 8001`
3. [ ] 启动前端: `cd src/dashboard && npm run dev`
4. [ ] 访问 http://localhost:5173 确认 Dashboard 加载
5. [ ] 访问 http://localhost:8001/ 确认 API 响应
6. [ ] 运行一次全量扫描: `.\aaq_full_audit.bat`
7. [ ] 确认 `data/AAQ_Report_*.md` 已生成

## 上线后监控

- [ ] 检查 `logs/` 目录无错误日志
- [ ] 确认 Dashboard 数据刷新正常
- [ ] 确认告警通知正常触发
- [ ] 24 小时内无异常崩溃

## 回滚方案

```bash
git log --oneline -5         # 查看最近提交
git revert <commit-hash>     # 回滚特定提交
git push                     # 推送回滚
```

## 已知限制 (v1.0)

| 编号 | 说明 | 优先级 | 计划版本 |
|------|------|--------|----------|
| P0 | Jisilu 数据需要 Cookie (当前用 AkShare) | Known | v2.0 |
| P1 | 自动化回退为模拟模式 | Known | v2.0 |
| P2 | 策略阈值硬编码 | Medium | v2.0 |
| P2 | 报告格式待美化 | Low | v2.0 |
