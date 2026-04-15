# Engineering Standard

## 核心架构原则

### 1. Agent Centralization
- 所有Agent通信必须通过Hermes ACP Server
- 禁止Agent间直接通信
- 使用标准化JSON消息格式

### 2. Protocol Stability
- WebSocket协议版本化，向后兼容
- 消息格式变更需要版本号递增
- 适配器层隔离外部依赖

### 3. Port Isolation
- Hermes ACP Server: 33333
- Claude Code: 3001
- Windsurf: 3000
- Antigravity: 3002
- Gemini CLI: 3004 (待安装)

## 代码结构标准

### Python模块结构
```
src/
├── acp_server/              # ACP Server核心
│   ├── __init__.py
│   ├── server.py           # WebSocket服务器
│   ├── message_handler.py  # 消息处理
│   └── session_manager.py  # 会话管理
├── adapters/               # Agent适配器
│   ├── __init__.py
│   ├── base_adapter.py    # 基础适配器类
│   ├── claude_adapter.py  # Claude Code适配器
│   ├── windsurf_adapter.py # Windsurf适配器
│   ├── gemini_adapter.py  # Gemini CLI适配器
│   └── antigravity_adapter.py # Antigravity适配器
├── bridge_manager/         # 桥接管理器
│   ├── __init__.py
│   ├── orchestrator.py    # 任务编排
│   ├── coordinator.py     # Agent协调
│   └── dispatcher.py      # 任务分发
└── utils/                  # 工具函数
    ├── __init__.py
    ├── logger.py          # 日志工具
    ├── config.py          # 配置管理
    └── validators.py      # 验证工具
```

### Node.js模块结构
```
src/
├── server.js              # Express服务器
├── websocket/             # WebSocket处理
│   ├── connection.js     # 连接管理
│   ├── protocol.js       # 协议实现
│   └── handlers.js       # 消息处理器
├── agents/               # Agent客户端
│   ├── base_agent.js     # 基础Agent类
│   └── agent_factory.js  # Agent工厂
└── utils/                # 工具函数
    ├── logger.js         # 日志
    ├── config.js         # 配置
    └── health.js         # 健康检查
```

## WebSocket协议标准

### 消息格式
```json
{
  "version": "2.1",
  "type": "task_request|task_response|status_update|coordination_request",
  "agent": "agent_name",
  "session_id": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    // 具体消息内容
  }
}
```

### 消息类型定义
- `task_request`: Agent请求任务执行
- `task_response`: Agent返回任务结果
- `status_update`: Agent状态更新
- `coordination_request`: 多Agent协调请求
- `heartbeat`: 心跳消息
- `error`: 错误消息

### 错误处理标准
```json
{
  "version": "2.1",
  "type": "error",
  "agent": "agent_name",
  "session_id": "uuid",
  "timestamp": "ISO8601",
  "payload": {
    "error_code": "VALIDATION_FAILED",
    "error_message": "详细错误描述",
    "context": "错误上下文信息",
    "suggestions": ["建议解决方案1", "建议解决方案2"]
  }
}
```

## Agent适配器标准

### 基础适配器接口
```python
class BaseAdapter:
    def __init__(self, agent_name: str, port: int):
        self.agent_name = agent_name
        self.port = port
        self.connection = None
    
    async def connect(self) -> bool:
        """连接到Agent"""
        pass
    
    async def send_task(self, task: dict) -> dict:
        """发送任务给Agent"""
        pass
    
    async def get_status(self) -> dict:
        """获取Agent状态"""
        pass
    
    async def disconnect(self):
        """断开连接"""
        pass
```

### 适配器实现要求
- 继承BaseAdapter类
- 实现所有抽象方法
- 包含错误处理和重连机制
- 支持心跳检测
- 记录详细日志

## 配置管理标准

### 配置文件结构
```json
{
  "acp_server": {
    "host": "localhost",
    "port": 33333,
    "max_connections": 100
  },
  "agents": {
    "claude_code": {
      "port": 3001,
      "timeout": 30,
      "retry_count": 3
    },
    "windsurf": {
      "port": 3000,
      "timeout": 30,
      "retry_count": 3
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/acp.log",
    "max_size": "10MB",
    "backup_count": 5
  }
}
```

### 环境变量标准
- `ACP_CONFIG_PATH`: 配置文件路径
- `ACP_LOG_LEVEL`: 日志级别
- `ACP_ENVIRONMENT`: 环境(dev/test/prod)
- `OBSIDIAN_VAULT_PATH`: Obsidian工作区路径

## 日志标准

### 日志级别
- `DEBUG`: 详细调试信息
- `INFO`: 一般信息记录
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `CRITICAL`: 严重错误

### 日志格式
```
[2026-04-15 22:10:30] [INFO] [AGENT:claude_code] [TASK:task_001] Connected successfully
[2026-04-15 22:10:31] [ERROR] [AGENT:windsurf] [TASK:task_002] Connection timeout after 30s
```

### 日志文件管理
- 按日期轮转：`acp_2026-04-15.log`
- 最大文件大小：10MB
- 保留最近30天日志
- 错误日志单独记录：`acp_error.log`

## 测试工程标准

### 单元测试要求
- 每个模块必须有对应测试文件
- 测试覆盖率不低于80%
- 使用mock隔离外部依赖
- 包含边界条件测试

### 集成测试要求
- 测试Agent与ACP Server连接
- 测试WebSocket消息传输
- 测试多Agent协作场景
- 包含异常情况测试

### 性能测试要求
- 连接建立时间 < 1秒
- 消息响应延迟 < 500ms
- 支持至少10个并发Agent
- 内存使用稳定

## 安全标准

### 认证机制
- Agent连接时验证身份
- 使用token-based认证
- 定期轮换认证token
- 记录认证失败日志

### 数据安全
- 敏感数据加密存储
- 传输数据使用TLS
- 定期备份重要配置
- 访问权限最小化

### 网络安全
- 限制端口访问范围
- 使用防火墙保护
- 定期安全扫描
- 及时更新依赖包

## 性能优化标准

### 资源使用限制
- ACP Server内存使用 < 512MB
- 单个Agent适配器内存 < 64MB
- CPU使用率 < 50%
- 网络带宽 < 10Mbps

### 优化策略
- 使用连接池管理WebSocket连接
- 异步处理消息队列
- 缓存频繁访问的配置
- 定期清理无用会话

## 监控和告警标准

### 关键指标监控
- Agent连接数
- 消息处理延迟
- 错误率统计
- 资源使用情况

### 告警规则
- Agent连接失败超过3次
- 消息处理延迟超过2秒
- 错误率超过5%
- 系统资源使用超过80%

### 健康检查
- 每30秒检查Agent状态
- 每分钟检查系统资源
- 每小时检查日志错误
- 每天生成健康报告
