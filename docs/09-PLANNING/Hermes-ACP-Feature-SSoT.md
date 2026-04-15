# Feature SSoT - Hermes ACP Ecosystem

> 单一事实源：管理所有 feature / wave / implementation 的进度和 residual。
> 开始任何非平凡任务前先读这个文件，完成后必须回写。

**最后更新**: 2026-04-15 22:30:00
**版本**: v1.0
**维护Agent**: Claude Code

## Active Features

| ID | Feature | Status | Task Plan | Worktree | Primary Agent | Residual | Updated |
|----|---------|--------|-----------|----------|---------------|----------|---------|
| F-001 | Harness Bootstrap | 🟡 进行中 | `docs/09-PLANNING/TASKS/2026-04-15-infra-harness-bootstrap` | `agent/TASK-001/claude` | Claude Code | Phase 8-11 待完成 | 2026-04-15 |
| F-002 | Agent Priority Queue | 🔴 未开始 | `docs/09-PLANNING/TASKS/2026-04-16-feat-agent-priority-queue` | 未创建 | Windsurf | 待开始 | 2026-04-15 |
| F-003 | WebSocket Protocol v2.1 | 🔴 未开始 | 待创建 | 未创建 | Hermes + Claude | 待开始 | 2026-04-15 |
| F-004 | Obsidian Integration v2 | 🟡 进行中 | `docs/09-PLANNING/TASKS/2026-04-10-feat-obsidian-sync-v2` | `agent/TASK-004/windsurf` | Windsurf | 同步优化中 | 2026-04-10 |
| F-005 | Multi-Agent Monitoring Dashboard | 🔴 未开始 | 待创建 | 未创建 | Gemini CLI | 待开始 | 2026-04-15 |

## Completed Features

| ID | Feature | Completed | Walkthrough | Primary Agent |
|----|---------|-----------|-------------|---------------|
| C-001 | Basic ACP Server Setup | 2026-04-01 | `docs/10-WALKTHROUGH/2026-04-01-acp-server-setup.md` | Hermes |
| C-002 | Claude Code Adapter | 2026-04-03 | `docs/10-WALKTHROUGH/2026-04-03-claude-adapter.md` | Claude Code |
| C-003 | Windsurf Adapter | 2026-04-05 | `docs/10-WALKTHROUGH/2026-04-05-windsurf-adapter.md` | Windsurf |
| C-004 | Basic WebSocket Protocol | 2026-04-07 | `docs/10-WALKTHROUGH/2026-04-07-websocket-protocol.md` | Hermes |
| C-005 | Agent Connection Monitor | 2026-04-09 | `docs/10-WALKTHROUGH/2026-04-09-connection-monitor.md` | Claude Code |

## On-Hold Features

| ID | Feature | Status | Pause Reason | Resume Date |
|----|---------|--------|-------------|-------------|
| H-001 | Advanced AI Routing | ⏸ 暂停 | 需要优先完成Harness基础设施 | 待定 |
| H-002 | Performance Optimization | ⏸ 暂停 | 等待Harness完成后进行 | 待定 |

## Cancelled Features

| ID | Feature | Cancelled | Reason |
|----|---------|-----------|--------|
| X-001 | Legacy Agent Support | 2026-04-02 | 架构不兼容，采用新适配器模式 |
| X-002 | Direct Database Integration | 2026-04-04 | 安全风险，改为通过Obsidian集成 |

## Status Legend

- 🔴 **未开始**: 任务已规划但未开始执行
- 🟡 **进行中**: 任务正在执行中
- 🟢 **已完成**: 任务完成并通过所有验收标准
- ⏸ **暂停**: 任务暂时停止，有明确的恢复计划
- ❌ **已取消**: 任务被取消，有明确的取消原因

## Priority Matrix

### High Priority (P1)
- Agent系统稳定性相关
- WebSocket协议核心功能
- 生产环境安全问题

### Medium Priority (P2)
- 性能优化和改进
- 新功能开发
- 用户体验改进

### Low Priority (P3)
- 实验性功能
- 文档完善
- 工具和脚本优化

## Agent Workload Distribution

| Agent | Active Tasks | Completed Tasks | Capacity |
|-------|-------------|----------------|----------|
| Hermes | 1 | 2 | 80% |
| Gemini CLI | 1 | 0 | 90% |
| Claude Code | 1 | 2 | 70% |
| Windsurf | 1 | 1 | 75% |
| Antigravity | 0 | 0 | 100% |

## Upcoming Milestones

### v1.1 - Harness Integration (Target: 2026-04-20)
- [ ] Complete Phase 7-11 of Harness Bootstrap
- [ ] Establish full Regression System
- [ ] Implement Walkthrough Process
- [ ] Deploy Worktree Standards

### v1.2 - Agent Enhancement (Target: 2026-04-30)
- [ ] Implement Agent Priority Queue
- [ ] Upgrade WebSocket Protocol to v2.1
- [ ] Enhanced Multi-Agent Monitoring
- [ ] Performance Optimization

### v1.3 - Integration Expansion (Target: 2026-05-15)
- [ ] Obsidian Integration v2
- [ ] Advanced AI Routing
- [ ] External API Integrations
- [ ] Security Enhancements

## Dependencies and Blockers

### Current Blockers
- **F-001**: Harness Bootstrap must complete before other features can proceed
- **F-004**: Obsidian sync issues blocking documentation workflow

### Dependencies
- **F-002** depends on **F-001** completion
- **F-003** depends on **F-001** completion
- **F-005** depends on **F-002** and **F-003** completion

## Risk Assessment

### High Risk Items
- **WebSocket Protocol Stability**: Core communication layer, any failure affects all agents
- **Multi-Agent Coordination**: Complex interaction patterns, potential for race conditions
- **Performance Under Load**: System may degrade with multiple concurrent agents

### Mitigation Strategies
- Comprehensive regression testing (Evidence Depth L4)
- Staged rollout with rollback capability
- Performance monitoring and alerting

## Quality Metrics

### Completion Rate
- **Overall**: 75% (5 completed / 8 total)
- **This Month**: 60% (3 completed / 5 planned)
- **On-Time Delivery**: 80%

### Evidence Depth Achievement
- **L1 (Unit Tests)**: 100% of completed features
- **L2 (Integration)**: 100% of completed features  
- **L3 (Live Environment)**: 80% of completed features
- **L4 (Production Smoke)**: 60% of completed features

## Update Guidelines

### When to Update
- Task status changes
- New tasks created or cancelled
- Milestones completed or delayed
- Agent workload changes

### How to Update
1. Update the corresponding row in the table
2. Update the "Last Updated" timestamp
3. Notify relevant agents through ACP
4. Update any dependent tasks

### Review Schedule
- **Daily**: Agent status and task progress
- **Weekly**: Feature prioritization and milestone review
- **Monthly**: Overall project health and risk assessment
