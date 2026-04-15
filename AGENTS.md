# Hermes ACP Ecosystem Bridge

> 这是 agent 进入项目时看到的第一个文件。它是目录和宪章，不是百科全书。

## 项目概况

- **项目名**：Hermes ACP Ecosystem Bridge
- **技术栈**：Python (主要) + Node.js (bridge服务) + WebSocket通信 + Express.js
- **仓库类型**：单仓（monorepo风格，多组件集成）
- **主要模块**：
  - Hermes ACP Server (Port 33333) - 中央协调服务器
  - Agent Adapters - 各AI代理适配器层
  - ACP Bridge Manager - 多代理协调器
  - WebSocket通信协议 - 标准化消息层
  - 监控和日志系统 - 系统健康检查

## 硬规则

以下规则绝对不能违反：

1. **WebSocket协议稳定性**: 所有agent通信必须通过标准化的JSON消息格式，不允许直接修改消息结构
2. **ACP Central Coordination**: 所有多agent协作必须通过Hermes ACP Server，不允许agent间直接通信
3. **Port隔离原则**: 各agent使用固定端口（Hermes:33333, Claude Code:3001, Windsurf:3000, Antigravity:3002, Gemini CLI:3004），不允许动态分配
4. **Backward Compatibility**: 修改adapter接口时必须保持向后兼容，使用版本化机制
5. **Security Boundary**: 所有外部集成必须通过adapter层隔离，不允许直接调用外部API

## Task-Type Reading Matrix

做什么类型的任务，先读哪个文件：

| 任务类型 | 先读 |
|----------|------|
| Hermes ACP Server / 核心通信协议 | `docs/11-REFERENCE/engineering-standard.md` |
| Agent Adapter 开发 / 修改 | `docs/11-REFERENCE/engineering-standard.md` |
| WebSocket 消息格式 / 协议修改 | `docs/11-REFERENCE/api-standard.md` |
| 测试 / 冒烟 / 回归 / agent连接检查 | `docs/11-REFERENCE/testing-standard.md` |
| 开发执行 / commit / PR / 代码规范 | `docs/11-REFERENCE/execution-workflow-standard.md` |
| 文档治理 / planning / 任务管理 | `docs/11-REFERENCE/docs-library-standard.md` |
| 回归 SSoT 维护 / Evidence Depth | `docs/11-REFERENCE/regression-ssot-governance.md` |
| Walkthrough 收口 / 任务完成记录 | `docs/11-REFERENCE/walkthrough-standard.md` |
| Worktree 操作 / 多agent并行开发 | `docs/11-REFERENCE/worktree-standard.md` |
| Obsidian 集成 / 外部文档同步 | `docs/11-REFERENCE/integration-standard.md` |
| 安全策略 / 权限管理 / 审计 | `docs/11-REFERENCE/security-standard.md` |

## Agent Roles & Responsibilities

### 🤖 Windsurf - 主执行者
- **职责**: 主要代码执行和开发任务
- **上下文**: 通过ACP Bridge接收项目上下文
- **优先级**: P2（主要执行agent）

### 🧠 Gemini CLI - 主协调器  
- **职责**: 项目规划、任务分解、中央协调
- **上下文**: 通过ACP Server协调所有Agent
- **优先级**: P1（主要协调agent）

### 🔍 Claude Code - 代码审查员
- **职责**: 代码质量保证和安全性审查
- **上下文**: 通过ACP Bridge接收代码变更
- **优先级**: P2（质量保证）

### 🛠️ OpenClaw - 自动化执行者
- **职责**: 自动化脚本执行和测试部署
- **上下文**: 通过ACP Bridge接收执行任务
- **优先级**: P3（自动化任务）

### 🤖 Antigravity - 创意探索者
- **职责**: 创意性研究和创意生成
- **上下文**: 通过ACP Bridge接收探索需求
- **优先级**: P3（研究任务）

## 开发流程

1. 非平凡任务先建 task plan（`docs/09-PLANNING/TASKS/`）
2. 回写 Feature SSoT
3. 开 worktree，分支隔离（多agent并行时使用agent专用分支）
4. 完成后 merge + 跑回归（按 Cadence Ledger）
5. 写 walkthrough（`docs/10-WALKTHROUGH/`）
6. 清理 worktree

## SSoT 文件

- **Feature SSoT**：`docs/09-PLANNING/Hermes-ACP-Feature-SSoT.md`
- **Regression SSoT**：`docs/05-TEST-QA/Regression-SSoT.md`
- **Cadence Ledger**：`docs/05-TEST-QA/Cadence-Ledger.md`

## 协作规则

### Multi-Agent并行协议
- **Agent优先级**: P1 > P2 > P3，资源冲突时高优先级优先
- **Worktree命名**: `agent/{task-id}/{agent-name}`，例如 `agent/TASK-001/windsurf`
- **通信协议**: 所有agent间通信必须通过Hermes ACP Server广播
- **状态同步**: 每30秒自动同步agent状态到ACP Monitor

### Merge审批流程
- **P1任务**: 需要至少1个P2 agent审查
- **Core协议修改**: 需要所有P2 agent审查 + P1确认
- **Security相关修改**: 需要Claude Code强制审查

### Evidence Depth要求
- **L1**: Unit tests（所有adapter）
- **L2**: Integration tests（WebSocket通信）
- **L3**: Agent connection tests（5个agent全连接）
- **L4**: Production smoke tests（完整ACP生态）

## 关键Surface清单

1. **Hermes ACP Server** (Port 33333) - 核心协调服务
2. **WebSocket通信协议** - 标准化JSON消息
3. **Agent Adapters** - 5个AI代理适配器
4. **ACP Bridge Manager** - 多代理任务分发
5. **监控日志系统** - 系统健康检查
6. **Obsidian集成** - 外部文档同步
