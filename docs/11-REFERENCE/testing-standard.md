# Testing Standard

## 测试框架
- 单元测试：pytest (Python) + jest (Node.js)
- 集成测试：pytest + WebSocket测试库
- 端到端测试：自定义ACP连接测试套件

## 测试目录结构
```
tests/
├── unit/                     # 单元测试
│   ├── test_acp_server.py
│   ├── test_agent_adapters.py
│   └── test_bridge_manager.py
├── integration/              # 集成测试
│   ├── test_websocket_protocol.py
│   ├── test_agent_communication.py
│   └── test_obsidian_sync.py
├── e2e/                      # 端到端测试
│   ├── test_full_acp_ecosystem.py
│   └── test_multi_agent_workflow.py
├── fixtures/                 # 测试数据
│   ├── mock_agent_responses.json
│   └── test_acp_messages.json
└── conftest.py              # pytest配置
```

## 命名规范
- 测试文件：`test_*.py` (Python) / `*.test.js` (Node.js)
- 测试用例：描述性命名，`test_should_[expected_behavior]_when_[condition]`
- 测试类：`Test[ModuleName]`

## 覆盖率要求
- 核心模块（ACP Server, Bridge Manager）：85%
- Agent Adapters：80%
- WebSocket协议层：90%
- 工具函数：75%

## 冒烟测试
- 入口命令：`python -m pytest tests/smoke/ -v`
- 覆盖范围：
  - Hermes ACP Server启动 (Port 33333)
  - 5个Agent连接检查
  - WebSocket消息格式验证
  - 基础消息收发测试
- 执行时机：每次merge到主干前

## Evidence Depth分级

### L1: Unit Tests
- 所有adapter层的独立功能测试
- ACP Server核心逻辑测试
- Bridge Manager任务分发测试

### L2: Integration Tests  
- WebSocket通信协议测试
- Agent与ACP Server连接测试
- 消息序列化/反序列化测试

### L3: Live Environment Tests
- 5个Agent同时连接测试
- 多Agent并行任务测试
- Obsidian workspace集成测试

### L4: Production Smoke Tests
- 完整ACP生态系统启动
- 真实Agent工作流测试
- 外部集成点健康检查

## 回归测试
- 参考 `docs/05-TEST-QA/Regression-SSoT.md`
- 按Cadence Ledger规则触发

## 测试编写原则
1. 每个测试只验证一件事
2. 测试之间互相独立，不依赖执行顺序
3. 使用fixture管理测试数据，不硬编码
4. mock外部依赖（如Obsidian API），不mock内部实现
5. 测试失败时的错误信息要有诊断价值
6. WebSocket测试使用真实的WebSocket库，避免过度mock

## Agent连接测试标准
```python
def test_agent_connection_standard():
    """标准Agent连接测试模板"""
    # 1. 检查Agent端口可用性
    # 2. 验证WebSocket握手
    # 3. 测试标准消息格式
    # 4. 验证agent身份认证
    # 5. 测试心跳机制
```

## 性能测试基准
- ACP Server启动时间：< 3秒
- Agent连接建立时间：< 1秒  
- 消息响应延迟：< 500ms
- 并发连接数：支持至少10个Agent

## 测试环境配置
- 测试端口：33334 (ACP Server), 3003-3007 (Agents)
- 测试Workspace：`tests/fixtures/test_workspace/`
- Mock Obsidian Vault：`tests/fixtures/mock_obsidian/`
