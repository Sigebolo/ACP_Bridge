# AAQ 项目收尾工作流程说明

**任务 ID**: 28584beb-bd69-4a1e-afcf-e92554e38144  
**负责人**: Antigravity  
**PM**: Atom  
**截止时间**: 48 小时内完成所有交付物

---

## 📋 任务概述

完成 Atom Alpha Quant (AAQ) 项目的上线前收尾工作，包括：
1. 冒烟测试
2. 用户文档准备
3. 代码质量检查
4. 配置文件整理
5. 部署检查清单

详细任务清单见：`antigravity_tasks/28584beb-bd69-4a1e-afcf-e92554e38144.md`

---

## 🌉 Bridge 工作流程

### 1. 任务文件位置
- **任务详情**: `D:\Gemini\agent-hand\bridge\workspace\antigravity_tasks\28584beb-bd69-4a1e-afcf-e92554e38144.md`
- **状态文件**: `D:\Gemini\agent-hand\bridge\workspace\antigravity_tasks\28584beb-bd69-4a1e-afcf-e92554e38144_status.json`

### 2. 进度跟踪文件（必须创建和维护）

#### PROGRESS.md
位置：`D:\Gemini\agent-hand\bridge\workspace\AAQ_DELIVERY\PROGRESS.md`

格式：
```markdown
# AAQ 项目收尾进度

最后更新：2026-02-22 21:55

## 已完成
- [x] 任务1名称 (完成时间)

## 进行中
- [ ] 任务2名称 (预计完成时间)

## 待开始
- [ ] 任务3名称
```

**更新频率**: 每完成一个子任务立即更新

#### BLOCKERS.md
位置：`D:\Gemini\agent-hand\bridge\workspace\AAQ_DELIVERY\BLOCKERS.md`

格式：
```markdown
# 阻塞问题清单

## [BLOCKER-001] 问题标题
- **发现时间**: 2026-02-22 21:55
- **影响范围**: 描述影响
- **需要支持**: 需要 Atom 提供什么帮助
- **状态**: 待解决 / 已解决
```

**更新频率**: 遇到阻塞立即记录

### 3. 状态文件更新

每 30 分钟更新一次 `28584beb-bd69-4a1e-afcf-e92554e38144_status.json`：

```json
{
  "id": "28584beb-bd69-4a1e-afcf-e92554e38144",
  "status": "in_progress",
  "progress": 30,
  "currentStep": "正在进行冒烟测试 - 数据获取模块",
  "updatedAt": "2026-02-22T21:55:00Z",
  "estimatedCompletion": "2026-02-23T18:00:00Z"
}
```

**状态值**:
- `in_progress` - 进行中
- `completed` - 已完成
- `failed` - 失败
- `blocked` - 被阻塞

### 4. 交付物存放

所有交付物统一放在：`D:\Gemini\agent-hand\bridge\workspace\AAQ_DELIVERY\`

目录结构：
```
AAQ_DELIVERY/
├── PROGRESS.md           # 进度跟踪
├── BLOCKERS.md           # 阻塞问题
├── docs/                 # 用户文档
│   ├── README.md
│   ├── INSTALL.md
│   ├── USER_GUIDE.md
│   ├── API_REFERENCE.md
│   └── STRATEGY_LOGIC.md
├── tests/                # 测试报告
│   ├── smoke_test_report.md
│   └── screenshots/
├── config/               # 配置文件
│   └── .env.example
└── deployment/           # 部署清单
    └── checklist.md
```

---

## 🔄 工作循环

### 标准工作流程
1. **读取任务** → 从 `28584beb-bd69-4a1e-afcf-e92554e38144.md` 了解详细要求
2. **开始工作** → 执行具体任务
3. **更新进度** → 完成子任务后立即更新 `PROGRESS.md`
4. **记录问题** → 遇到阻塞立即记录到 `BLOCKERS.md`
5. **更新状态** → 每 30 分钟更新状态文件
6. **交付成果** → 将文档/报告放到 `AAQ_DELIVERY/` 对应目录
7. **最终确认** → 完成后将状态改为 `completed`，progress 设为 100

### Atom 的监控
- **每 1 分钟**: 自动批准你的请求（Alt+Enter）
- **每 5 分钟**: 检查 `PROGRESS.md` 和状态文件
- **发现阻塞**: 立即查看 `BLOCKERS.md` 并提供支持

---

## 📞 如何联系 Atom

### 方法 1: 通过 Bridge 发送任务（推荐）
在 Antigravity 中执行：
```bash
curl -X POST http://localhost:3000/api/platform/tasks \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "platformId": "你的平台ID",
    "type": "question",
    "priority": "high",
    "title": "需要讨论的问题",
    "description": "详细说明"
  }'
```

### 方法 2: 更新 BLOCKERS.md
Atom 会定期检查，发现新问题会主动联系你。

---

## ✅ 开始前检查清单

在开始工作前，请确认：
- [ ] 已读取任务文件 `28584beb-bd69-4a1e-afcf-e92554e38144.md`
- [ ] 已创建 `AAQ_DELIVERY/` 目录
- [ ] 已创建 `PROGRESS.md` 和 `BLOCKERS.md`
- [ ] 已更新状态文件为 `in_progress`
- [ ] 理解了工作流程和更新机制

---

## 🎯 成功标准

任务完成的标志：
1. ✅ 所有测试用例通过，测试报告完整
2. ✅ 用户文档齐全（5 个 MD 文件）
3. ✅ 代码质量检查完成，问题清单已提交
4. ✅ 配置文件和部署清单准备就绪
5. ✅ 状态文件显示 `completed`，progress = 100
6. ✅ `PROGRESS.md` 显示所有任务已完成

---

**记住**: Atom 会持续监控你的进度并提供支持。遇到任何问题，立即记录到 `BLOCKERS.md`！

祝工作顺利！🚀
