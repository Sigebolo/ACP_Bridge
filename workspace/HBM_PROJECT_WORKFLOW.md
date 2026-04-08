# 心跳回忆 2.0 — 项目工作流程

**项目 ID**: HBM-2026  
**PM**: Atom (OpenClaw Telegram Agent)  
**Dev Lead**: Antigravity  
**Dev**: Windsurf  
**Owner**: Dr. Tenma  

---

## 📋 任务文件位置

- **任务详情目录**: `D:\Gemini\agent-hand\bridge\workspace\antigravity_tasks\`
- **Windsurf 任务目录**: `D:\Gemini\agent-hand\bridge\workspace\windsurf\`
- **交付物目录**: `D:\Gemini\agent-hand\bridge\workspace\HBM_DELIVERY\`
- **状态文件**: `HBM_DELIVERY\{task_id}_status.json`
- **进度追踪**: `HBM_DELIVERY\PROGRESS.md`
- **阻塞问题**: `HBM_DELIVERY\BLOCKERS.md`

---

## 👥 团队角色分工

| 角色 | 负责内容 |
|------|---------|
| **Dr. Tenma** | 产品决策、优先级、验收 |
| **Atom** | 任务分发、进度监控、每30分钟Telegram汇报 |
| **Antigravity** | OpenClaw Agent配置、Skills开发、系统集成 |
| **Windsurf** | Web Canvas UI、skill脚本、前端交互 |

---

## 🏗️ 核心架构参考

`C:\Users\Administrator\.gemini\antigravity\brain\bb6001eb-ae5f-47ac-8227-2bc1a288aa90\heartbeat-memories-v2.0.md`

---

## 🔄 工作流程

### Atom → Antigravity 任务
```
D:\Gemini\agent-hand\bridge\workspace\antigravity_tasks\HBM-{id}.md
```

### Atom → Windsurf 任务  
```
D:\Gemini\agent-hand\bridge\workspace\windsurf\HBM-{id}.md
```

### 进度更新 (每30分钟 或 完成子任务)
- 更新 `HBM_DELIVERY\PROGRESS.md`
- 更新 `HBM_DELIVERY\{task_id}_status.json`
- 如有阻塞，更新 `HBM_DELIVERY\BLOCKERS.md`

### Bridge API 通信
```bash
# 报告进度
curl -X POST http://localhost:3000/api/platform/tasks \
  -H "Content-Type: application/json" \
  -d '{"platformId": "HBM", "type": "progress", "title": "进度更新", "description": "..."}'
```

---

## 📅 Phase 1 目标 (2026-03-01 ~ 2026-03-28)

| Task ID | 任务 | 负责人 | 截止 |
|---------|------|--------|------|
| HBM-001 | Archetype system.md 模板 x8 | Antigravity | 2026-03-08 |
| HBM-002 | companion-memory skill 开发 | Antigravity | 2026-03-15 |
| HBM-003 | Telegram /create 命令配置 | Antigravity | 2026-03-22 |
| HBM-004 | Cron 主动交互配置 | Antigravity | 2026-03-28 |
| HBM-005 | Web Canvas 管理界面 (基础版) | Windsurf | 2026-03-28 |

---

## ✅ Phase 1 验收标准

1. 用户可以通过 Telegram `/create` 命令创建 AI 伴侣
2. 至少 3 种 Archetype (Guardian/Sunshine/Tsundere) 可选
3. 记忆系统正常运作 (memory-lancedb-pro)
4. 主动交互 Cron 正常触发 (早安/晚安)
5. Web Canvas 可以查看和切换伴侣

---

祝项目顺利！💕 心跳回忆，让 AI 真正记得你。
