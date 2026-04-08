# OpenClaw Bridge Service

本地桥接服务，用于OpenClaw PM系统与各种编程平台之间的通信和协作。

## 功能特性

- **双向通信**: OpenClaw与编程平台之间的实时双向通信
- **状态管理**: 实时跟踪任务状态和进度
- **文件管理**: 支持artifacts的上传、下载和管理
- **通知系统**: 实时通知和事件广播
- **多平台支持**: 支持Google CLI、Windsurf等多种编程平台
- **决策管理**: OpenClaw负责所有决策制定

## 架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OpenClaw PM   │◄──►│  Bridge Service │◄──►│  Programming    │
│   (决策层)      │    │   (桥接层)      │    │  Platforms      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Storage &      │
                       │  Notification   │
                       │  Services       │
                       └─────────────────┘
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动服务

```bash
# 开发模式
npm run dev

# 生产模式
npm start
```

服务将在以下端口启动：
- REST API: `http://localhost:3000`
- WebSocket: `ws://localhost:3001`

## API 文档

### OpenClaw PM 接口

#### 创建需求
```http
POST /api/pm/requirements
Content-Type: application/json

{
  "title": "用户登录功能",
  "description": "实现用户登录和认证功能",
  "priority": "high",
  "category": "authentication",
  "requirements": [
    "支持邮箱登录",
    "支持密码重置",
    "支持记住登录状态"
  ],
  "acceptanceCriteria": [
    "用户可以使用邮箱和密码登录",
    "登录失败有明确的错误提示",
    "登录成功后跳转到首页"
  ]
}
```

#### 获取需求列表
```http
GET /api/pm/requirements?status=pending&priority=high
```

#### 制定决策
```http
POST /api/pm/decisions
Content-Type: application/json

{
  "title": "选择前端框架",
  "description": "为新项目选择合适的前端框架",
  "options": [
    {"name": "React", "pros": ["生态丰富", "社区活跃"], "cons": ["学习曲线陡峭"]},
    {"name": "Vue", "pros": ["易学易用", "文档完善"], "cons": ["生态相对较小"]}
  ],
  "selectedOption": "React",
  "rationale": "考虑到项目复杂度和团队技能，选择React更合适"
}
```

### 平台接口

#### 注册平台
```http
POST /api/platform/register
Content-Type: application/json

{
  "name": "Google CLI Platform",
  "type": "google-cli",
  "description": "Google Cloud CLI集成平台",
  "capabilities": ["deployment", "infrastructure", "monitoring"],
  "config": {
    "project": "my-project",
    "region": "us-central1",
    "auth": {
      "credentials": "path/to/credentials.json"
    }
  }
}
```

#### 获取平台任务
```http
GET /api/platform/tasks/{platformId}?status=pending
```

#### 完成任务
```http
POST /api/platform/tasks/{platformId}/complete
Content-Type: application/json

{
  "taskId": "task-uuid",
  "result": {
    "status": "success",
    "output": "Deployment completed successfully",
    "metrics": {
      "duration": 120000,
      "resourcesCreated": 5
    }
  },
  "artifacts": [
    {
      "name": "deployment-log.txt",
      "content": "Deployment log content...",
      "type": "log"
    }
  ]
}
```

### 状态和Artifacts

#### 获取全局状态
```http
GET /api/status
```

#### 获取Artifacts
```http
GET /api/artifacts?taskId=task-uuid&type=log
```

#### 下载Artifact
```http
GET /api/artifacts/{artifactId}
```

## WebSocket 通信

### 连接
```javascript
const ws = new WebSocket('ws://localhost:3001');

ws.onopen = () => {
  // 订阅通知
  ws.send(JSON.stringify({
    type: 'subscribe',
    filters: {
      types: ['requirement_created', 'task_completed', 'artifact_uploaded'],
      priority: 'high'
    }
  }));
};
```

### 消息格式
```javascript
// 状态更新
{
  "type": "status_update",
  "taskId": "task-uuid",
  "status": "in_progress",
  "progress": 75
}

// Artifact通知
{
  "type": "artifact_notification",
  "artifact": {
    "id": "artifact-uuid",
    "name": "build-output.zip",
    "type": "archive"
  }
}
```

## 支持的平台

### Google CLI
- **功能**: 部署、基础设施管理、监控、数据处理
- **配置**: 需要Google Cloud认证和项目配置
- **任务类型**: deployment, infrastructure, monitoring, data_processing

### Windsurf
- **功能**: 代码开发、测试、分析、重构
- **配置**: 需要API端点和认证密钥
- **任务类型**: development, testing, code_analysis, refactoring

## 配置说明

### 环境变量
```bash
PORT=3000                    # REST API端口
WS_PORT=3001                 # WebSocket端口
NODE_ENV=development         # 运行环境
LOG_LEVEL=info              # 日志级别
```

### 配置文件
配置文件位于 `config/default.json`，包含：
- 服务器设置
- 数据库配置
- 平台配置
- 安全设置
- 日志配置

## 数据存储

### 目录结构
```
bridge/
├── data/                   # 数据文件
│   ├── requirements.json
│   ├── decisions.json
│   ├── platforms.json
│   ├── tasks.json
│   └── artifacts.json
├── artifacts/              # 文件存储
├── workspace/              # 平台工作空间
│   ├── google-cli/
│   └── windsurf/
└── logs/                   # 日志文件
```

## 监控和日志

### 健康检查
```http
GET /health
```

### 日志级别
- `error`: 错误信息
- `warn`: 警告信息
- `info`: 一般信息
- `debug`: 调试信息

## 安全考虑

1. **API认证**: 可配置API密钥认证
2. **文件上传**: 限制文件类型和大小
3. **速率限制**: 防止API滥用
4. **CORS配置**: 跨域请求控制

## 故障排除

### 常见问题

1. **平台连接失败**
   - 检查平台配置
   - 验证认证信息
   - 确认网络连接

2. **任务执行失败**
   - 查看任务日志
   - 检查平台状态
   - 验证输入参数

3. **通知未收到**
   - 检查WebSocket连接
   - 验证订阅过滤器
   - 确认客户端状态

## 开发指南

### 添加新平台适配器

1. 在 `src/adapters/platforms/` 创建新适配器
2. 实现必需方法：`initialize`, `assignTask`, `getStatus`
3. 在 `PlatformAdapterManager` 中注册适配器
4. 更新配置文件

### 扩展通知类型

1. 在 `NotificationService` 中添加新方法
2. 定义通知数据格式
3. 更新客户端处理逻辑

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
