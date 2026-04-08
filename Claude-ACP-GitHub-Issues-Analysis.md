# Claude Agent ACP GitHub踩坑总结

## 发现的关键问题

### 1. session/new参数问题 ✅ 已踩坑
**Issue #491**: ACP session initialization fails with third-party models
- **错误**: `Invalid input: expected object, received undefined`
- **原因**: 缺少必需的`cwd`和`mcpServers`参数
- **状态**: 这正是我们遇到的问题！

### 2. JSON解析问题 ✅ 已踩坑  
**Issue #493**: CLI output was not valid JSON
- **错误**: `{"jsonrpc":"2.0","id":5,"error":{"code":-32603,"message":"Internal error"...}}`
- **原因**: Claude Agent启动时的JSON输出解析问题
- **影响**: 可能导致通信中断

### 3. 第三方模型兼容性 ✅ 已踩坑
**Issue #491详细分析**:
- **问题**: 使用DashScope等第三方模型时初始化失败
- **根本原因**: 新版本移除了Bailian/DashScope的workaround代码
- **解决方案**: 需要恢复第三方模型检测和处理逻辑

## Claude官方文档指引

### MCP服务器配置格式
根据Claude官方文档，正确的session/new参数格式：

```json
{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "session/new",
  "params": {
    "cwd": "d:/Gemini/agent-hand/bridge",
    "mcpServers": [],
    "capabilities": ["file_access", "terminal", "tools", "streaming"]
  }
}
```

### MCP服务器配置示例
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

## 我们的修复方案

### 1. 立即修复 ✅
- 添加`cwd`参数到session/new请求
- 添加`mcpServers: []`参数到session/new请求
- 使用正确的消息格式

### 2. 消息格式修复
根据官方文档，正确的prompt格式：
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "消息内容"
          }
        ]
      }
    ]
  }
}
```

### 3. 错误处理
- 捕获JSON解析错误
- 实现重试机制
- 添加详细日志记录

## 验证步骤

### 1. 测试修复后的连接
```bash
python connect_to_claude_acp_fixed.py
```

### 2. 检查Claude响应
- 确认10秒内收到响应
- 验证响应内容正确性
- 确认无错误输出

### 3. 集成到ACP Bridge
- 更新acp_bridge_manager.py中的Claude配置
- 确保所有参数格式正确
- 测试完整的事件流程

## 结论

**✅ 这些都是已知问题，有官方解决方案！**

**🎯 我们的实现方向正确**：
- 问题识别准确
- 修复方案明确
- 有官方文档支持

**🚀 可以立即实施修复**，Claude Agent ACP应该能正常工作！

---
*基于GitHub官方issue和文档分析*
