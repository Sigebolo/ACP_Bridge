# Regression SSoT Governance

## Regression SSoT概述

Regression SSoT (Single Source of Truth) 是项目回归测试的单一数据源，用于：
- 定义所有回归测试的触发条件和执行标准
- 跟踪回归测试的历史记录和趋势
- 确保测试覆盖的一致性和完整性
- 为Evidence Depth分级提供依据

## SSoT文件结构

### 主文件: `docs/05-TEST-QA/Regression-SSoT.md`

```markdown
# Regression SSoT

最后更新: 2026-04-15
版本: v2.1
维护Agent: Claude Code

## Evidence Depth矩阵

| Surface | L1 Unit | L2 Integration | L3 Live | L4 Production | 触发条件 |
|---------|---------|----------------|---------|---------------|----------|
| Hermes ACP Server | ✅ | ✅ | ✅ | ✅ | 每次commit |
| Agent Adapters | ✅ | ✅ | ✅ | 🔄 | 适配器修改 |
| WebSocket Protocol | ✅ | ✅ | ✅ | ✅ | 协议变更 |
| Bridge Manager | ✅ | ✅ | 🔄 | 🔄 | 核心逻辑修改 |
| Obsidian Integration | ✅ | 🔄 | 🔄 | 🔄 | 集成修改 |
| Monitoring System | ✅ | ✅ | 🔄 | 🔄 | 监控修改 |

图例: ✅ 必需执行 / 🔄 条件执行 / ⭕ 可选执行
```

## Cadence Ledger集成

### 触发规则映射
```markdown
## Cadence Ledger触发映射

| 触发事件 | Evidence Depth | 执行频率 | 负责Agent |
|----------|----------------|----------|-----------|
| commit到main | L1 | 实时 | 自动 |
| PR创建 | L1+L2 | 按需 | Claude Code |
| 适配器修改 | L1+L2+L3 | 按需 | Windsurf |
| 协议版本变更 | L1+L2+L3+L4 | 强制 | 所有Agent |
| 发布候选 | L1+L2+L3+L4 | 强制 | Claude Code |
| 紧急修复 | L1+L2 | 立即 | 相关Agent |
```

## Surface详细定义

### 1. Hermes ACP Server (Port 33333)
**关键功能**: 中央协调服务器，WebSocket通信核心
**回归要求**:
- L1: 核心逻辑单元测试
- L2: WebSocket协议集成测试
- L3: 多Agent并发连接测试
- L4: 生产环境冒烟测试

**测试套件**:
```bash
# L1
python -m pytest tests/unit/test_acp_server.py

# L2  
python -m pytest tests/integration/test_websocket_protocol.py

# L3
python -m pytest tests/e2e/test_multi_agent_connection.py

# L4
python scripts/production_smoke_test.py
```

### 2. Agent Adapters
**关键功能**: 各AI代理适配器层
**回归要求**:
- L1: 每个适配器独立测试
- L2: 与ACP Server集成测试
- L3: 真实Agent连接测试
- L4: 生产环境Agent健康检查

**测试覆盖**:
- Claude Code Adapter (Port 3001)
- Windsurf Adapter (Port 3000)
- Antigravity Adapter (Port 3002)
- Gemini CLI Adapter (Port 3004)

### 3. WebSocket Protocol
**关键功能**: 标准化JSON消息格式
**回归要求**:
- L1: 消息序列化/反序列化测试
- L2: 端到端消息传输测试
- L3: 多Agent消息广播测试
- L4: 生产环境消息延迟测试

**版本兼容性**:
- v2.1: 当前生产版本
- v2.0: 向后兼容版本
- v1.x: 已弃用版本

### 4. Bridge Manager
**关键功能**: 多代理协调和任务分发
**回归要求**:
- L1: 任务分发逻辑测试
- L2: Agent协调集成测试
- L3: 并行任务执行测试
- L4: 生产环境负载测试

### 5. Obsidian Integration
**关键功能**: 外部文档和项目管理集成
**回归要求**:
- L1: 文档同步逻辑测试
- L2: Obsidian API集成测试
- L3: 真实工作区同步测试
- L4: 生产环境文档一致性检查

### 6. Monitoring System
**关键功能**: 系统健康检查和监控
**回归要求**:
- L1: 监控逻辑单元测试
- L2: 监控数据收集测试
- L3: Agent状态监控测试
- L4: 生产环境告警测试

## Evidence Depth详细标准

### L1: Unit Tests (单元测试)
**目标**: 验证单个函数/类的正确性
**覆盖率要求**: 80%+
**执行频率**: 每次commit
**工具**: pytest (Python), jest (Node.js)

**质量标准**:
- 每个测试独立运行
- Mock外部依赖
- 包含边界条件
- 错误处理测试

### L2: Integration Tests (集成测试)
**目标**: 验证模块间交互正确性
**覆盖率要求**: 关键路径100%
**执行频率**: PR创建时
**工具**: pytest + WebSocket测试库

**质量标准**:
- 真实环境配置
- 端到端消息流测试
- 错误恢复测试
- 性能基准测试

### L3: Live Environment Tests (生产环境测试)
**目标**: 验证在类生产环境中的稳定性
**覆盖率要求**: 核心功能100%
**执行频率**: 重要变更后
**工具**: 真实Agent + 生产配置

**质量标准**:
- 使用真实Agent连接
- 模拟生产负载
- 长时间稳定性测试
- 资源使用监控

### L4: Production Smoke Tests (生产冒烟测试)
**目标**: 验证生产环境基本功能正常
**覆盖率要求**: 关键路径100%
**执行频率**: 每次发布
**工具**: 生产环境脚本

**质量标准**:
- 生产环境数据
- 真实用户场景
- 性能回归检查
- 安全扫描

## 回归执行流程

### 自动触发流程
1. **代码变更检测**: Git hook检测到变更
2. **Surface识别**: 根据变更文件识别影响Surface
3. **Depth确定**: 根据变更类型确定Evidence Depth
4. **测试执行**: 自动执行对应级别的测试
5. **结果记录**: 更新Regression SSoT
6. **通知机制**: 通过ACP通知相关Agent

### 手动触发流程
1. **Agent请求**: Agent通过ACP请求回归测试
2. **影响评估**: 评估变更影响范围
3. **测试计划**: 制定测试执行计划
4. **执行测试**: 按计划执行测试
5. **结果分析**: 分析测试结果
6. **更新SSoT**: 更新Regression SSoT记录

## 回归结果管理

### 结果记录格式
```markdown
## 回归执行记录

### 执行信息
- **时间**: 2026-04-15 22:30:00
- **触发原因**: PR #123 - 修复Claude适配器连接问题
- **执行Agent**: Claude Code
- **Evidence Depth**: L1+L2+L3

### 测试结果
| Surface | L1 | L2 | L3 | L4 | 状态 |
|---------|----|----|----|----|------|
| Hermes ACP Server | ✅ | ✅ | ✅ | N/A | PASS |
| Agent Adapters | ✅ | ✅ | ✅ | N/A | PASS |
| WebSocket Protocol | ✅ | ✅ | ✅ | N/A | PASS |

### 发现的问题
1. **问题**: Agent连接超时偶发
   - **严重程度**: Medium
   - **影响**: 5%的连接请求
   - **解决方案**: 增加重试机制

### 性能指标
- **总执行时间**: 15分钟
- **L1测试**: 2分钟 (120个测试)
- **L2测试**: 8分钟 (45个测试)
- **L3测试**: 5分钟 (10个测试)
```

### 趋势分析
```markdown
## 回归趋势分析

### 最近30天统计
- **总执行次数**: 45次
- **通过率**: 95.6%
- **平均执行时间**: 12分钟
- **失败率最高Surface**: Agent Adapters (8%)

### 性能趋势
- **L1平均时间**: 稳定在2分钟
- **L2平均时间**: 从10分钟优化到8分钟
- **L3平均时间**: 稳定在5分钟
```

## 回归失败处理

### 失败分类
1. **Critical**: 生产功能失效
2. **High**: 核心功能受影响
3. **Medium**: 次要功能问题
4. **Low**: 非功能性问题

### 处理流程
1. **立即通知**: 通过ACP通知相关Agent
2. **问题定位**: 分析失败原因
3. **修复方案**: 制定修复计划
4. **验证修复**: 重新执行回归测试
5. **更新记录**: 更新Regression SSoT

### 回滚策略
- **Critical失败**: 立即回滚到上一个稳定版本
- **High失败**: 评估影响后决定是否回滚
- **Medium失败**: 继续发布但制定修复计划
- **Low失败**: 记录问题，后续修复

## SSoT维护规范

### 更新频率
- **实时更新**: 测试执行结果
- **每日汇总**: 当天测试统计
- **每周回顾**: 周度趋势分析
- **每月报告**: 月度质量报告

### 维护职责
- **日常维护**: 自动化脚本更新
- **质量分析**: Claude Code负责
- **趋势监控**: Windsurf负责
- **性能优化**: Gemini CLI负责

### 版本控制
- **文件版本**: 每次重要更新递增
- **变更记录**: 记录所有重要变更
- **备份策略**: 保留最近30天历史
- **恢复机制**: 支持版本回滚

## 回归优化策略

### 执行优化
- **并行测试**: 多个Surface并行执行
- **智能缓存**: 缓存测试结果和依赖
- **增量测试**: 只执行受影响的测试
- **优先级队列**: 重要测试优先执行

### 资源优化
- **测试环境**: 使用容器化测试环境
- **资源调度**: 合理分配测试资源
- **清理机制**: 及时清理测试临时文件
- **监控告警**: 监控测试资源使用

### 质量优化
- **测试覆盖率**: 持续提高测试覆盖率
- **测试质量**: 定期review测试用例
- **自动化程度**: 提高测试自动化水平
- **反馈速度**: 缩短测试反馈时间

## 集成工具和脚本

### 回归执行脚本
```bash
#!/bin/bash
# run-regression.sh

SURFACE=$1
DEPTH=$2
TRIGGER=$3

echo "Running regression for $SURFACE at depth $DEPTH"

case $DEPTH in
  "L1")
    python -m pytest tests/unit/test_${SURFACE,,}.py
    ;;
  "L2")
    python -m pytest tests/integration/test_${SURFACE,,}.py
    ;;
  "L3")
    python -m pytest tests/e2e/test_${SURFACE,,}.py
    ;;
  "L4")
    python scripts/production_smoke_${SURFACE,,}.py
    ;;
esac

# 更新Regression SSoT
python scripts/update_regression_ssot.py --surface $SURFACE --depth $DEPTH --result $?
```

### SSoT更新脚本
```python
# update_regression_ssot.py
import json
import datetime
import sys

def update_ssot(surface, depth, result):
    # 读取当前SSoT
    with open('docs/05-TEST-QA/Regression-SSoT.md', 'r') as f:
        content = f.read()
    
    # 更新执行记录
    record = {
        'timestamp': datetime.datetime.now().isoformat(),
        'surface': surface,
        'depth': depth,
        'result': 'PASS' if result == 0 else 'FAIL',
        'trigger': sys.argv[4] if len(sys.argv) > 4 else 'manual'
    }
    
    # 写入更新
    # ... 实现更新逻辑
    
if __name__ == '__main__':
    update_ssot(sys.argv[2], sys.argv[4], int(sys.argv[6]))
```
