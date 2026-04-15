# Regression SSoT - Hermes ACP Ecosystem

> 单一事实源：管理所有 regression surface 的状态、证据深度和残项。
> 新增固定 gate 或 evidence depth 变化时必须更新。

**最后更新**: 2026-04-15 22:30:00
**版本**: v2.1
**维护Agent**: Claude Code

## Evidence Depth矩阵

| Surface ID | Surface Name | L1 Unit | L2 Integration | L3 Live | L4 Production | Status | Last Verified | Primary Agent |
|------------|--------------|---------|----------------|---------|---------------|---------|---------------|---------------|
| RG-001 | Hermes ACP Server | ✅ | ✅ | ✅ | ✅ | 🟢 | 2026-04-15 | Hermes |
| RG-002 | Claude Code Adapter | ✅ | ✅ | ✅ | 🔄 | 🟡 | 2026-04-14 | Claude Code |
| RG-003 | Windsurf Adapter | ✅ | ✅ | ✅ | 🔄 | 🟡 | 2026-04-13 | Windsurf |
| RG-004 | Antigravity Adapter | ✅ | ✅ | 🔄 | ⭕ | 🟡 | 2026-04-12 | Antigravity |
| RG-005 | Gemini CLI Adapter | ✅ | 🔄 | ⭕ | ⭕ | 🔴 | 2026-04-10 | Gemini CLI |
| RG-006 | WebSocket Protocol | ✅ | ✅ | ✅ | ✅ | 🟢 | 2026-04-15 | Hermes |
| RG-007 | Bridge Manager | ✅ | ✅ | 🔄 | ⭕ | 🟡 | 2026-04-14 | Claude Code |
| RG-008 | Obsidian Integration | ✅ | 🔄 | ⭕ | ⭕ | 🔴 | 2026-04-09 | Windsurf |
| RG-009 | Monitoring System | ✅ | ✅ | 🔄 | ⭕ | 🟡 | 2026-04-11 | Gemini CLI |
| RG-010 | Security Layer | ✅ | ✅ | 🔄 | ⭕ | 🟡 | 2026-04-15 | Claude Code |

**图例**: ✅ 必需执行 / 🔄 条件执行 / ⭕ 可选执行 / 🔴 失败 / 🟡 部分通过 / 🟢 全部通过

## Active Fixed Gates

| ID | Status | Surface | Primary Entrypoint | Evidence Depth | Last Verified | Execution Time | Notes |
|----|--------|---------|-------------------|----------------|---------------|---------------|-------|
| RG-001 | 🟢 | Hermes ACP Server | `python -m pytest tests/unit/test_acp_server.py && python scripts/acp_server_integration.py` | L4 | 2026-04-15 | 15m | Production ready |
| RG-002 | 🟡 | Claude Code Adapter | `python -m pytest tests/unit/test_claude_adapter.py && python scripts/claude_live_test.py` | L3 | 2026-04-14 | 8m | L4 pending production access |
| RG-003 | 🟡 | Windsurf Adapter | `python -m pytest tests/unit/test_windsurf_adapter.py && python scripts/windsurf_live_test.py` | L3 | 2026-04-13 | 7m | L4 pending production access |
| RG-006 | 🟢 | WebSocket Protocol | `python -m pytest tests/integration/test_websocket_protocol.py && python scripts/production_smoke_websocket.py` | L4 | 2026-04-15 | 12m | All message types verified |

## Evidence Depth详细定义

| Level | Name | Description | Execution Environment | Tools |
|-------|------|-------------|----------------------|-------|
| L1 | tests | 单元测试，验证单个函数/类的正确性 | Local/CI | pytest, jest |
| L2 | integration | 集成测试，验证模块间交互 | Local/CI | pytest, WebSocket Test Library |
| L3 | live | 真实环境测试，使用真实Agent连接 | Staging | Real Agents, Staging Environment |
| L4 | production | 生产环境冒烟测试，验证关键功能 | Production | Production Scripts, Monitoring |

## Cadence Ledger触发规则

| Surface | Trigger Event | Auto Execute | Evidence Depth | Responsible Agent |
|---------|---------------|--------------|----------------|-------------------|
| RG-001 | commit到main | ✅ | L1 | 自动 |
| RG-001 | PR创建 | ✅ | L1+L2 | Claude Code |
| RG-001 | 适配器修改 | ✅ | L1+L2+L3 | Windsurf |
| RG-001 | 协议版本变更 | ✅ | L1+L2+L3+L4 | 所有Agent |
| RG-002 | adapter代码变更 | ✅ | L1+L2 | Claude Code |
| RG-002 | Claude Code版本更新 | ✅ | L1+L2+L3 | Claude Code |

## Residual Items

| ID | Surface | Issue | Priority | Severity | Created | Target Resolution | Assigned Agent |
|----|---------|-------|----------|----------|---------|-------------------|---------------|
| R-001 | RG-005 | Gemini CLI Adapter连接超时 | P1 | High | 2026-04-10 | 2026-04-20 | Gemini CLI |
| R-002 | RG-008 | Obsidian同步偶发失败 | P2 | Medium | 2026-04-09 | 2026-04-25 | Windsurf |
| R-003 | RG-007 | Bridge Manager内存泄漏 | P2 | Medium | 2026-04-14 | 2026-04-22 | Claude Code |
| R-004 | RG-004 | Antigravity Adapter不稳定 | P3 | Low | 2026-04-12 | 2026-05-01 | Antigravity |

## Performance Benchmarks

| Surface | Metric | Target | Current | Status | Last Measured |
|---------|--------|--------|---------|---------|---------------|
| RG-001 | Server启动时间 | < 3s | 2.1s | ✅ | 2026-04-15 |
| RG-001 | 消息处理延迟 | < 500ms | 380ms | ✅ | 2026-04-15 |
| RG-002 | Agent连接时间 | < 1s | 0.8s | ✅ | 2026-04-14 |
| RG-006 | 消息序列化时间 | < 50ms | 35ms | ✅ | 2026-04-15 |
| RG-009 | 监控数据收集延迟 | < 200ms | 180ms | ✅ | 2026-04-11 |

## 测试环境配置

### Local Development
- **Python**: 3.12+
- **Node.js**: 18+
- **Test Ports**: 33334 (ACP), 3003-3007 (Agents)
- **Test Workspace**: `tests/fixtures/test_workspace/`

### Staging Environment  
- **ACP Server**: staging.example.com:33333
- **Agents**: staging-agent-1.example.com (3000-3004)
- **Obsidian Vault**: staging-vault.obsidian.md
- **Monitoring**: staging-monitor.example.com

### Production Environment
- **ACP Server**: acp.hermes-ecosystem.com:33333
- **Agents**: agent-1.hermes-ecosystem.com (3000-3004)
- **Obsidian Vault**: production-vault.obsidian.md
- **Monitoring**: monitor.hermes-ecosystem.com

## 自动化执行脚本

### 回归测试主脚本
```bash
#!/bin/bash
# run-regression.sh

SURFACE=$1
DEPTH=$2
TRIGGER=$3

echo "Running regression for $SURFACE at depth $DEPTH"

case $SURFACE in
  "acp-server")
    python scripts/acp_server_regression.sh $DEPTH
    ;;
  "claude-adapter")
    python scripts/claude_adapter_regression.sh $DEPTH
    ;;
  "websocket-protocol")
    python scripts/websocket_protocol_regression.sh $DEPTH
    ;;
  *)
    echo "Unknown surface: $SURFACE"
    exit 1
esac

# 更新Regression SSoT
python scripts/update_regression_ssot.py --surface $SURFACE --depth $DEPTH --result $?
```

### 批量回归脚本
```bash
#!/bin/bash
# run-full-regression.sh

echo "Starting full regression suite..."

# L1 Tests - 所有surface
for surface in acp-server claude-adapter windsurf-adapter antigravity-adapter gemini-adapter websocket-protocol bridge-manager obsidian-integration monitoring-system security-layer; do
  echo "Running L1 for $surface..."
  python scripts/run_regression.py $surface L1 auto
done

# L2 Tests - 核心surface
for surface in acp-server claude-adapter windsurf-adapter websocket-protocol bridge-manager; do
  echo "Running L2 for $surface..."
  python scripts/run_regression.py $surface L2 auto
done

# L3 Tests - 生产就绪surface
for surface in acp-server claude-adapter windsurf-adapter websocket-protocol; do
  echo "Running L3 for $surface..."
  python scripts/run_regression.py $surface L3 auto
done

# L4 Tests - 仅生产surface
for surface in acp-server websocket-protocol; do
  echo "Running L4 for $surface..."
  python scripts/run_regression.py $surface L4 auto
done

echo "Full regression completed"
```

## Status Legend

- 🟢 **通过**: 所有测试通过，无已知问题
- 🟡 **部分通过**: 主要测试通过，有已知残项
- 🔴 **失败**: 关键测试失败，需要立即修复
- ⏸ **暂停**: 测试暂时停止，有明确原因

## 质量趋势分析

### 最近30天统计
- **总执行次数**: 156次
- **通过率**: 87.2%
- **平均执行时间**: 11分钟
- **失败率最高Surface**: RG-005 (Gemini CLI Adapter) - 35%

### 性能趋势
- **L1平均时间**: 稳定在3分钟
- **L2平均时间**: 从12分钟优化到9分钟
- **L3平均时间**: 稳定在8分钟
- **L4平均时间**: 稳定在15分钟

### 改进措施
- 优化Gemini CLI Adapter连接稳定性
- 改进Obsidian同步错误处理
- 增强Bridge Manager内存管理
- 提升Antigravity Adapter可靠性

## 集成通知机制

### 失败通知
```python
# regression_failure_notification.py
def notify_failure(surface, depth, error_details):
    message = {
        "type": "regression_failure",
        "surface": surface,
        "depth": depth,
        "error": error_details,
        "timestamp": datetime.now().isoformat(),
        "assigned_agent": get_responsible_agent(surface)
    }
    
    # 通过ACP通知相关Agent
    acp_broadcast(message)
    
    # 发送邮件通知
    send_email_notification(message)
```

### 恢复通知
```python
def notify_recovery(surface, depth):
    message = {
        "type": "regression_recovery",
        "surface": surface,
        "depth": depth,
        "timestamp": datetime.now().isoformat(),
        "previous_failure": get_last_failure(surface)
    }
    
    acp_broadcast(message)
```

## 维护和更新

### 日常维护
- **自动更新**: 测试执行后自动更新状态
- **每日检查**: 检查失败和阻塞项目
- **每周回顾**: 分析趋势和改进机会
- **每月报告**: 生成质量报告

### 更新流程
1. **测试执行**: 自动或手动执行回归测试
2. **结果收集**: 收集所有测试结果
3. **状态更新**: 更新SSoT中的状态
4. **通知发送**: 通知相关Agent
5. **文档更新**: 更新相关文档

### 版本控制
- **文件版本**: 每次重要更新递增
- **变更记录**: 记录所有重要变更
- **备份策略**: 保留最近30天历史
- **恢复机制**: 支持版本回滚
