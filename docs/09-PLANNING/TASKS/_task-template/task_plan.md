# [任务名称]

## 目标
[一句话说清楚这个任务要达成什么]

## 范围
- 做什么：[具体范围]
- 不做什么：[明确排除]

## Agent分工
- **主要执行Agent**: [Agent名称]
- **协作Agent**: [Agent列表]
- **审查Agent**: [Agent列表]

## 步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 验收标准
- [ ] [标准1]
- [ ] [标准2]
- [ ] [标准3]

## Evidence Depth要求
- **L1 (Unit Tests)**: [是否需要]
- **L2 (Integration)**: [是否需要]
- **L3 (Live Environment)**: [是否需要]
- **L4 (Production Smoke)**: [是否需要]

## Worktree
- 路径：agent/[TASK-ID]/[agent-name]
- 分支：feature/[TASK-ID]-[agent-name]
- 若未开 worktree，原因：[说明]

## 关联
- Feature SSoT 条目：[引用]
- 相关 Regression Gate：[引用]
- 前置任务：[引用，如无则写"无"]
- 相关Walkthrough：[完成后填写]

## ACP协作
- **通信协议**: [使用的ACP消息类型]
- **状态同步频率**: [如每30分钟]
- **冲突解决策略**: [高优先级Agent优先等]

## 预估工期
- **预计开始时间**: [日期]
- **预计完成时间**: [日期]
- **复杂度**: [Low/Medium/High]

## 风险评估
- **技术风险**: [技术实现风险]
- **协作风险**: [多Agent协作风险]
- **依赖风险**: [外部依赖风险]
