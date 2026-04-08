# Gemini CLI ACP 文档分析总结

## 官方文档发现

### 1. Gemini CLI ACP架构
根据[geminicli.com/docs/cli/acp-mode/](https://geminicli.com/docs/cli/acp-mode/)：

#### **核心方法**
- `initialize` - 建立初始连接
- `authenticate` - 用户认证
- `newSession` - 开始新聊天会话
- `loadSession` - 加载之前的会话
- `prompt` - 发送提示给代理
- `cancel` - 取消进行中的提示

#### **会话控制**
- `setSessionMode` - 更改工具调用的批准级别
- `unstable_setSessionModel` - 更改当前会话的模型

#### **文件系统代理**
- ACP包含代理文件系统服务
- 代理通过ACP客户端读写文件
- 安全特性：确保代理只能访问用户明确允许的文件

### 2. 通信协议
- **传输方式**: 标准输入输出(stdio)
- **协议**: JSON-RPC 2.0
- **实现位置**: `packages/cli/src/acp/acpClient.ts`

### 3. Gemini CLI vs Claude Agent ACP 格式差异

#### **Gemini CLI期望格式**
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id",
    "prompt": "简单字符串消息"
  }
}
```

#### **Claude Agent ACP期望格式**
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id",
    "prompt": [
      {
        "role": "user",
        "content": "简单字符串消息"
      }
    ]
  }
}
```

### 4. 当前问题分析

#### **Gemini CLI问题**
- ✅ 初始化成功
- ✅ 会话创建成功
- ❌ 消息格式错误：期望简单字符串，收到复杂结构

#### **Claude Agent ACP问题**
- ✅ 初始化成功
- ✅ 会话创建成功
- ❌ 内容格式错误：期望特定结构，收到错误格式

### 5. 修复方案

#### **Gemini CLI修复**
```python
# 使用简单字符串
prompt_request = {
    "jsonrpc": "2.0",
    "id": "3",
    "method": "session/prompt",
    "params": {
        "sessionId": session_id,
        "prompt": "简单字符串消息"
    }
}
```

#### **Claude Agent ACP修复**
```python
# 使用简单字符串content
prompt_request = {
    "jsonrpc": "2.0",
    "id": "3",
    "method": "session/prompt",
    "params": {
        "sessionId": session_id,
        "prompt": [
            {
                "role": "user",
                "content": "简单字符串消息"
            }
        ]
    }
}
```

### 6. 实施建议

#### **立即行动**
1. **修复Claude Agent ACP** - 使用简单字符串content
2. **修复Gemini CLI** - 使用简单字符串prompt
3. **测试两个代理** - 确保10秒响应

#### **长期优化**
1. **统一消息格式** - 创建适配器处理不同格式
2. **错误处理** - 实现重试和降级机制
3. **配置管理** - 支持多代理动态切换

### 7. 结论

**✅ 两个ACP代理都有官方文档支持**
**✅ 问题格式已知，修复方案明确**
**✅ 可以立即实施修复**

**🚀 ACP Bridge架构完全可行，只需要调整消息格式！**

---
*基于Gemini CLI官方文档分析*
