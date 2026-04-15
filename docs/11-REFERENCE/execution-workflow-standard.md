# Execution Workflow Standard

## 开发执行流程

### 开始任务前
1. 读Feature SSoT (`docs/09-PLANNING/Hermes-ACP-Feature-SSoT.md`)，确认任务状态
2. 读对应的task_plan.md，对齐目标
3. 确认是否需要开worktree（参考worktree-standard.md）
4. 如需开worktree，按规范创建并记录
5. 检查ACP生态系统状态：`python acp_ecosystem_monitor.py`

### 执行过程中
1. 每完成一个阶段，更新progress.md
2. 研究发现写入findings.md
3. 定期commit，commit message有意义
4. 遇到阻塞，立即记录到progress.md并通过ACP报告
5. 多Agent协作时，通过Hermes ACP Server同步状态

### 完成任务后
1. 确保所有改动已commit，工作区clean
2. 跑对应的回归测试（按Cadence Ledger）
3. 更新Feature SSoT
4. 写walkthrough（参考walkthrough-standard.md）
5. 如有worktree，按规范清理
6. 通过ACP向相关Agent发送完成通知

## Commit规范

格式：`<type>(<scope>): <description>`

Type：
- `feat`: 新功能
- `fix`: Bug修复
- `refactor`: 重构
- `test`: 测试
- `docs`: 文档
- `chore`: 构建/工具/配置
- `perf`: 性能优化
- `acp`: ACP相关修改

Scope：模块或Agent名
- `hermes`: Hermes ACP Server
- `bridge`: ACP Bridge Manager
- `adapter/{agent}`: 特定Agent适配器
- `protocol`: WebSocket协议
- `monitor`: 监控系统

示例：
- `feat(hermes): add agent priority queue system`
- `fix(adapter/claude): resolve message encoding issue`
- `test(protocol): add websocket message validation tests`
- `docs(walkthrough): standardize multi-agent completion format`

## PR/Merge规范

1. PR标题遵循commit规范格式
2. PR描述包含：
   - 改了什么
   - 为什么改
   - 怎么验证的
   - 影响的Agent和Surface
3. 引用对应的task plan和Feature SSoT条目
4. 回归测试结果附在PR中（包含Evidence Depth级别）
5. Multi-Agent协作任务需要所有相关Agent确认

## Agent协作执行规范

### 任务分发流程
1. PM Agent（通常是Hermes）创建任务计划
2. 通过ACP Server广播任务给相关Agent
3. Agent确认接收并分配优先级
4. 按优先级顺序执行，实时同步进度

### 并行开发规则
- 每个Agent使用独立的worktree
- 共享资源修改需要通过ACP协调
- 冲突时高优先级Agent优先
- 所有协议修改需要P2级别Agent审查

### 状态同步要求
- 每30秒自动同步Agent状态
- 关键节点立即广播
- 阻塞问题5分钟内上报
- 完成任务后发送标准化完成消息

## 禁止事项

- 禁止在项目根目录放过程文件（task_plan、progress等只能在任务目录内）
- 禁止跳过task plan直接开始非平凡任务
- 禁止merge后不跑回归
- 禁止merge后不写walkthrough
- 禁止Agent间直接通信，必须通过ACP Server
- 禁止修改核心WebSocket协议版本号
- 禁止在代码中硬编码Agent端口

## 紧急修复流程

对于生产环境紧急问题：
1. 创建hotfix worktree
2. 修复后立即运行L1-L2回归测试
3. 通过ACP快速通知所有Agent
4. 24小时内补全walkthrough和完整回归

## 质量门禁

- 所有代码变更必须通过L1测试
- 协议层修改必须通过L2测试
- Agent适配器修改必须通过L3测试
- 生产发布前必须通过L4测试

## 工具链集成

- Pre-commit hooks：运行flake8, black, pytest
- CI/CD：自动触发Evidence Depth测试
- ACP集成：自动状态同步和通知
- 文档生成：自动更新AGENTS.md索引
