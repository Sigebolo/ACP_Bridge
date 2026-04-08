# Bridge 通讯规则（标准模板）

**重要提醒**：每次任务开始前，请仔细阅读本规则。你可能缺乏之前的记忆，这些规则会帮助你正确协作。

---

## 📋 任务状态文件

**位置**：`{task_id}_status.json`

**格式**：
```json
{
  "id": "{task_id}",
  "status": "in_progress",  // pending | in_progress | completed | failed | blocked
  "progress": 30,           // 0-100
  "currentStep": "正在进行冒烟测试 - 数据获取模块",
  "updatedAt": "2026-02-22T22:00:00Z",
  "estimatedCompletion": "2026-02-23T18:00:00Z"
}
```

**更新频率**：每 30 分钟更新一次，或完成重要子任务时立即更新

---

## 📝 进度跟踪文件

**位置**：`{delivery_folder}/PROGRESS.md`

**格式**：
```markdown
# {项目名称} 进度

最后更新：2026-02-22 22:00

## 已完成 ✅
- [x] 任务1名称 (完成时间: 2026-02-22 20:30)
- [x] 任务2名称 (完成时间: 2026-02-22 21:15)

## 进行中 🔄
- [ ] 任务3名称 (预计完成: 2026-02-22 23:00)

## 待开始 ⏳
- [ ] 任务4名称
- [ ] 任务5名称
```

**更新频率**：每完成一个子任务立即更新

---

## 🚫 阻塞问题文件

**位置**：`{delivery_folder}/BLOCKERS.md`

**格式**：
```markdown
# 阻塞问题清单

## [BLOCKER-001] 问题标题
- **发现时间**: 2026-02-22 22:00
- **影响范围**: 描述影响（如：无法继续测试模块 X）
- **需要支持**: 需要 Atom 提供什么帮助
- **状态**: 待解决 / 已解决
- **解决时间**: (已解决时填写)

## [BLOCKER-002] 另一个问题
...
```

**更新频率**：遇到阻塞立即记录，解决后立即更新状态

---

## 📦 交付物存放

**位置**：`{delivery_folder}/`

**目录结构**：
```
{delivery_folder}/
├── PROGRESS.md           # 进度跟踪
├── BLOCKERS.md           # 阻塞问题
├── docs/                 # 文档
├── tests/                # 测试报告
├── config/               # 配置文件
└── deployment/           # 部署相关
```

**规则**：
- 所有交付物必须放在指定目录
- 文件命名清晰，使用英文或拼音
- 重要文件添加 README 说明

---

## 🔄 工作循环

### 标准流程
1. **读取任务** → 从任务文件了解详细要求
2. **开始工作** → 执行具体任务
3. **更新进度** → 完成子任务后立即更新 PROGRESS.md
4. **记录问题** → 遇到阻塞立即记录到 BLOCKERS.md
5. **更新状态** → 每 30 分钟更新状态文件
6. **交付成果** → 将文档/报告放到交付目录
7. **最终确认** → 完成后将状态改为 completed，progress 设为 100

### Atom PM 的监控
- **每 1 分钟**：检查是否需要批准（Alt+Enter）
- **每 3 分钟**：检查进度和阻塞情况
- **发现阻塞**：立即查看 BLOCKERS.md 并提供支持
- **任务完成**：验收交付物并报告给天马博士

---

## 📞 如何联系 Atom

### 方法 1：更新 BLOCKERS.md（推荐）
Atom 会定期检查，发现新问题会主动联系你。

### 方法 2：通过 Bridge API 发送任务
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

---

## ✅ 开始前检查清单

在开始工作前，请确认：
- [ ] 已读取任务文件
- [ ] 已创建交付目录
- [ ] 已创建 PROGRESS.md 和 BLOCKERS.md
- [ ] 已更新状态文件为 in_progress
- [ ] 理解了工作流程和更新机制

---

## 🎯 完成标准

任务完成的标志：
1. 所有子任务在 PROGRESS.md 中标记为 [x]
2. 状态文件显示 completed，progress = 100
3. 所有交付物已放入交付目录
4. BLOCKERS.md 中无未解决问题
5. 已通知 Atom 进行验收

---

**记住**：Atom 会持续监控你的进度并提供支持。遇到任何问题，立即记录到 BLOCKERS.md！

祝工作顺利！🚀
