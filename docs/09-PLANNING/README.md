# Planning Loop Index

## 概述

Planning Loop是Hermes ACP项目的任务管理和执行框架，确保每个非平凡任务都有明确的目标、过程跟踪和结果记录。

## 目录结构

```
docs/09-PLANNING/
├── README.md                    # 本文件，Planning Loop索引
├── Hermes-ACP-Feature-SSoT.md   # 功能排期单一数据源
├── TASKS/                       # 任务目录
│   └── _task-template/          # 任务模板
│       ├── task_plan.md         # 任务计划模板
│       ├── findings.md          # 研究发现模板
│       └── progress.md          # 进度跟踪模板
└── worktree-tracker.md          # Worktree跟踪记录
```

## 任务类型分类

### 按复杂度分类
- **Simple**: 单Agent，< 4小时，单一模块
- **Medium**: 多Agent协作，4-16小时，跨模块
- **Complex**: 多Agent并行，> 16小时，系统级变更

### 按类型分类
- **Feature**: 新功能开发
- **Bugfix**: 问题修复
- **Refactor**: 代码重构
- **Optimization**: 性能优化
- **Infrastructure**: 基础设施改进
- **Documentation**: 文档更新
- **Testing**: 测试改进
- **Security**: 安全相关

## 任务命名规范

### 格式: `YYYY-MM-DD-[类型]-[简短描述]`
- `YYYY-MM-DD`: 任务创建日期
- `[类型]`: 任务类型缩写 (feat, fix, ref, opt, infra, doc, test, sec)
- `[简短描述]`: 英文简短描述，用kebab-case

### 示例
- `2026-04-15-feat-agent-priority-queue`
- `2026-04-16-fix-websocket-timeout`
- `2026-04-17-ref-adapter-base-class`
- `2026-04-18-opt-message-processing`

## Planning Loop执行流程

### 1. 任务创建
```bash
# 创建任务目录
mkdir docs/09-PLANNING/TASKS/2026-04-15-feat-agent-priority-queue

# 复制模板文件
cp docs/09-PLANNING/TASKS/_task-template/* docs/09-PLANNING/TASKS/2026-04-15-feat-agent-priority-queue/

# 初始化task_plan.md
# 填写任务目标、范围、步骤等
```

### 2. Agent分配
- **主要执行Agent**: 负主要执行责任
- **协作Agent**: 提供支持和协作
- **审查Agent**: 负责质量审查

### 3. 执行跟踪
- 每个阶段开始前读task_plan.md
- 每个阶段完成后更新progress.md
- 重要研究发现写入findings.md

### 4. 状态同步
- 通过ACP Server同步Agent状态
- 每30分钟自动状态更新
- 阻塞问题立即上报

### 5. 任务完成
- 所有验收标准达成
- Evidence Depth测试通过
- Walkthrough文档完成
- 更新Feature SSoT

## Agent协作规范

### 协作场景
1. **串行协作**: Agent按顺序执行
2. **并行协作**: Agent同时工作不同模块
3. **审查协作**: Agent互相审查工作
4. **紧急协作**: 紧急问题快速响应

### 协作协议
- **任务分配**: 通过ACP Server广播
- **状态同步**: 定时heartbeat + 事件驱动
- **冲突解决**: 高优先级Agent优先
- **质量保证**: P2级别Agent强制审查

## 质量门禁

### 任务开始前
- [ ] task_plan.md完整填写
- [ ] Agent分工明确
- [ ] Worktree已创建
- [ ] 风险评估完成

### 执行过程中
- [ ] progress.md及时更新
- [ ] findings.md记录重要发现
- [ ] Evidence Depth逐步达成
- [ ] Agent状态正常同步

### 任务完成后
- [ ] 所有验收标准达成
- [ ] 测试覆盖完整
- [ ] Walkthrough文档完成
- [ ] Feature SSoT更新

## 模板使用指南

### task_plan.md
- **目标**: 一句话说清楚要达成什么
- **范围**: 明确做什么和不做什么
- **步骤**: 具体可执行的步骤
- **验收标准**: 可验证的完成标准
- **Agent分工**: 明确各Agent职责

### findings.md
- **研究发现**: 记录重要发现和决策
- **技术决策**: 记录技术选择和原因
- **协作发现**: 记录Agent协作经验
- **可复用模式**: 提炼可复用的模式

### progress.md
- **状态跟踪**: 实时更新任务状态
- **Evidence Depth**: 跟踪测试完成情况
- **阻塞问题**: 记录和解决阻塞
- **质量检查**: 确保质量标准

## 工具和脚本

### 任务创建脚本
```bash
#!/bin/bash
# create-task.sh
TASK_TYPE=$1
TASK_DESC=$2
TASK_DATE=$(date +%Y-%m-%d)
TASK_DIR="docs/09-PLANNING/TASKS/${TASK_DATE}-${TASK_TYPE}-${TASK_DESC}"

mkdir -p "$TASK_DIR"
cp docs/09-PLANNING/TASKS/_task-template/* "$TASK_DIR/"
echo "Task created: $TASK_DIR"
```

### 状态检查脚本
```bash
#!/bin/bash
# check-task-status.sh
find docs/09-PLANNING/TASKS -name "progress.md" -exec grep -l "状态：进行中" {} \;
```

## 监控和报告

### 日常监控
- **任务创建**: 每日新建任务数量
- **任务完成**: 每日完成任务数量
- **Agent负载**: 各Agent任务执行情况
- **阻塞问题**: 当前阻塞问题统计

### 周报模板
```markdown
# Planning Loop周报

## 任务统计
- **新建任务**: [数量]个
- **完成任务**: [数量]个
- **进行中**: [数量]个
- **阻塞任务**: [数量]个

## Agent表现
- **Windsurf**: [完成任务数]
- **Claude Code**: [完成任务数]
- **Gemini CLI**: [完成任务数]
- **Antigravity**: [完成任务数]

## 质量指标
- **平均工期**: [天数]
- **Evidence Depth达成率**: [百分比]
- **Walkthrough完成率**: [百分比]

## 改进建议
- [ ] [建议1]
- [ ] [建议2]
```

## 最佳实践

### 任务规划
- 目标要具体可衡量
- 范围要明确边界
- 步骤要可执行
- 验收标准要可验证

### Agent协作
- 明确分工和职责
- 保持及时沟通
- 尊重优先级规则
- 共享知识和经验

### 质量保证
- 严格按照模板执行
- 及时更新进度
- 记录重要发现
- 完成walkthrough

### 持续改进
- 定期回顾流程效果
- 优化模板和工具
- 积累最佳实践
- 提升协作效率
