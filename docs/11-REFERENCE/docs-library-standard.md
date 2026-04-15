# Docs Library Standard

## 文档治理原则

- **Agent First**: 所有文档首先为Agent可读性设计
- **按需加载**: Agent根据Task-Type Reading Matrix按需读取文档
- **版本化**: 所有重要文档必须有版本号和更新记录
- **可验证**: 文档中的流程必须可执行和验证

## 文档目录职责

### 00-RAW-PRDS/
- **用途**: 原始需求文档、PRD、用户故事
- **规范**: 按日期命名，如 `2026-04-15-user-story-xxx.md`
- **权限**: 只读，Agent不能直接修改

### 01-GOVERNANCE/
- **用途**: 项目治理规则、决策记录(ADR)
- **关键文件**: 
  - `decision-log.md` - 重要架构决策记录
  - `agent-collaboration-rules.md` - Agent协作规范

### 02-PRODUCT/
- **用途**: 产品设计、用户流程、功能规格
- **规范**: 按功能模块组织，每个功能一个文档

### 03-ARCHITECTURE/
- **用途**: 架构设计、技术方案、ADR
- **关键文件**:
  - `acp-protocol-design.md` - WebSocket协议设计
  - `agent-adapter-pattern.md` - 适配器设计模式
  - `system-architecture.md` - 整体架构图

### 04-DEVELOPMENT/
- **用途**: 开发指南、环境配置、本地开发说明
- **关键文件**:
  - `local-setup-guide.md` - 本地环境搭建
  - `agent-configuration.md` - Agent配置指南
  - `debugging-playbook.md` - 调试经验手册

### 05-TEST-QA/
- **用途**: 测试策略、Regression SSoT、Cadence Ledger
- **关键文件**:
  - `Regression-SSoT.md` - 回归测试单一数据源
  - `Cadence-Ledger.md` - 回归触发规则
  - `evidence-depth-standards.md` - Evidence Depth标准

### 06-INTEGRATIONS/
- **用途**: 第三方集成文档、API对接说明
- **关键文件**:
  - `obsidian-integration.md` - Obsidian集成文档
  - `external-api-standards.md` - 外部API标准

### 07-OPERATIONS/
- **用途**: 部署、运维、监控、告警
- **关键文件**:
  - `deployment-guide.md` - 部署指南
  - `monitoring-standards.md` - 监控标准

### 08-SECURITY/
- **用途**: 安全策略、权限模型、审计日志
- **关键文件**:
  - `agent-security-policy.md` - Agent安全策略
  - `websocket-security.md` - WebSocket安全规范

### 09-PLANNING/
- **用途**: 排期、任务计划
- **关键文件**:
  - `Hermes-ACP-Feature-SSoT.md` - 功能排期表
  - `TASKS/` - 任务目录，每个任务一个子目录

### 10-WALKTHROUGH/
- **用途**: Walkthrough收口记录
- **规范**: 按任务ID组织，如 `TASK-001-walkthrough.md`

### 11-REFERENCE/
- **用途**: 标准文件库，Agent按需加载
- **关键文件**: 所有工程标准和规范文档

### 99-TMP/
- **用途**: 临时文件，定期清理
- **清理规则**: 超过7天自动清理

## 文档命名规范

### 文件命名
- 使用kebab-case: `agent-adapter-pattern.md`
- 包含版本号: `acp-protocol-v2.1.md`
- 日期格式: `2026-04-15-decision-log.md`

### 目录命名
- 使用数字前缀排序: `01-GOVERNANCE/`
- 使用kebab-case: `agent-configuration/`

## 文档模板标准

### 每个文档必须包含:
```markdown
---
title: [文档标题]
version: [版本号]
last_updated: [更新日期]
responsible_agent: [负责Agent]
---

# [标题]

## 概述
[简要说明文档目的和范围]

## 适用场景
[什么情况下需要阅读此文档]

## 相关文档
- [相关文档链接]
```

### Task Plan模板
每个任务必须包含三件套:
- `task_plan.md` - 任务计划和目标
- `findings.md` - 研究发现和决策记录  
- `progress.md` - 进度跟踪和状态更新

## 文档更新流程

1. **Agent修改**: Agent根据任务需要修改文档
2. **版本记录**: 更新版本号和last_updated
3. **影响评估**: 评估对其他Agent的影响
4. **通知机制**: 通过ACP通知相关Agent
5. **归档**: 旧版本自动归档到`archive/`目录

## 文档质量标准

### 可读性要求
- 使用清晰的标题结构
- 代码块必须有语言标识
- 重要概念必须有定义
- 流程必须有步骤说明

### 可执行性要求
- 所有命令必须可复制执行
- 配置示例必须完整有效
- 流程步骤必须有验证方法

### Agent友好要求
- 避免模糊描述，要具体明确
- 提供Task-Type Reading Matrix索引
- 包含常见错误和解决方案

## 文档审查机制

### 审查触发条件
- 新文档创建
- 重要文档修改
- 跨Agent影响文档

### 审查流程
1. 作者Agent提交修改
2. 相关Agent审查（24小时内）
3. 治理Agent最终确认
4. 通过ACP发布更新通知

## 文档搜索和索引

### 关键词标准
- 每个文档必须有3-5个关键词
- 关键词要包含Agent名称和功能模块
- 使用标准化术语

### 索引维护
- AGENTS.md作为主索引
- 每个Reference文档在AGENTS.md中必须有入口
- 定期检查链接有效性
