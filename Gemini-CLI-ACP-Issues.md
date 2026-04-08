# Gemini CLI ACP 联调问题分析文档

## 问题描述

在实施ACP Bridge过程中，Gemini CLI的JSON-RPC消息格式存在兼容性问题，导致无法成功发送用户消息进行review。

## 问题详情

### 1. 初始化成功 ✅
```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "initialize",
  "params": {
    "protocolVersion": 1,
    "clientInfo": {
      "name": "ACP Bridge Review",
      "version": "1.0.0"
    },
    "capabilities": ["file_access", "terminal", "tools"]
  }
}
```
**状态**: ✅ 成功

### 2. 会话创建成功 ✅
```json
{
  "jsonrpc": "2.0",
  "id": "2",
  "method": "session/new",
  "params": {
    "cwd": "d:/Gemini/agent-hand/bridge",
    "mcpServers": [],
    "capabilities": ["file_access", "terminal", "tools"]
  }
}
```
**状态**: ✅ 成功，返回session_id

### 3. 消息发送失败 ❌
#### 尝试的格式1：简单字符串
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id_here",
    "prompt": "简单字符串消息"
  }
}
```
**错误**: `expected array, received string`

#### 尝试的格式2：数组格式
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id_here",
    "prompt": [
      {
        "role": "user",
        "content": "消息内容"
      }
    ]
  }
}
```
**错误**: `Invalid input: expected string, received undefined` (针对content字段)

#### 尝试的格式3：结构化content
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id_here",
    "prompt": [
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
**错误**: 多个字段缺失错误

## 错误分析

### Gemini CLI期望的格式
根据错误信息分析，Gemini CLI期望的content结构应该是：

```json
{
  "type": "text",
  "text": "实际文本内容"
}
```

### 当前问题
1. **协议版本**: 可能需要不同的protocolVersion
2. **内容结构**: content字段需要特定的type/text结构
3. **字段缺失**: 可能需要额外的必需字段

## 解决方案

### 方案1：研究Gemini CLI文档
```bash
# 查看Gemini CLI的ACP文档
npx @google/gemini-cli --help --experimental-acp
```

### 方案2：查看Gemini CLI源码
```bash
# 查看Gemini CLI的ACP实现
npm view @google/gemini-cli
```

### 方案3：使用其他工具逆向分析
```bash
# 使用Zed或其他IDE的Gemini集成作为参考
# 分析实际发送的消息格式
```

### 方案4：尝试不同的内容格式
```json
// 格式A：直接text字段
{
  "role": "user",
  "content": "直接文本内容"
}

// 格式B：完整结构
{
  "role": "user",
  "content": {
    "type": "text",
    "text": "消息内容"
  }
}

// 格式C：数组内容
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "消息内容"
    }
  ]
}
```

## 调试步骤

### 1. 启用详细日志
```bash
# 启动Gemini CLI时启用调试
DEBUG=acp:* npx @google/gemini-cli --experimental-acp
```

### 2. 捕获网络流量
```bash
# 使用工具监控stdio通信
# 分析实际的数据格式
```

### 3. 参考官方示例
```bash
# 查看官方ACP示例
curl https://agentclientprotocol.com/examples
```

## 临时解决方案

### 使用其他AI代理
1. **Claude Agent ACP** - 已编译完成，格式可能更标准
2. **自定义Antigravity ACP** - 完全控制消息格式
3. **等待Gemini CLI修复** - 这可能是Gemini CLI的bug

## 影响评估

### 当前影响
- ❌ 无法使用Gemini CLI进行review
- ✅ ACP Bridge架构完全正常
- ✅ 其他AI代理可以使用

### 业务影响
- **低**: ACP Bridge核心功能未受影响
- **可接受**: 有多个替代方案

## 下一步行动

### 立即行动
1. **部署Claude Agent ACP** - 开始实际使用
2. **完善自定义ACP服务器** - 确保完全可用
3. **记录问题** - 供后续参考

### 中期行动
1. **深入研究Gemini CLI格式**
2. **提交bug报告**（如果是Gemini CLI问题）
3. **更新ACP Bridge** 支持Gemini CLI

### 长期行动
1. **监控ACP协议演进**
2. **保持多代理兼容性**
3. **优化性能和稳定性**

#### 成功的格式：特定的Content Part结构
```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "method": "session/prompt",
  "params": {
    "sessionId": "session_id_here",
    "prompt": [
      {
        "type": "text",
        "text": "消息内容"
      }
    ]
  }
}
```
**状态**: ✅ 成功

## 错误分析（已解决）

### Gemini CLI期望的格式
1. **参数名**: 必须使用 `prompt` 而不是 `messages`。
2. **结构**: `prompt` 是一个对象数组，每个对象必须包含 `type` 字段（如 `"type": "text"`）和对应的内容字段（如 `"text": "..."`）。
3. **响应处理**: Gemini CLI 通过 `session/update` 通知发送流式的 `agent_message_chunk`，最终的 `result` 可能不包含完整内容，需要累积 chunks。

## 解决方案（已实施）

### ACP Bridge Manager 更新
已在 `acp_bridge_manager.py` 中实现了针对 Gemini CLI 的特殊处理：
1. **自动识别**: 根据代理名称识别 Gemini CLI。
2. **格式转换**: 自动将消息转换为 `prompt` 数组格式。
3. **响应累积**: 累积 `agent_message_chunk` 以提供完整的回复。

### 验证脚本
创建了 `test_correct_prompt.py` 和 `test_acp_bridge_with_gemini.py` 成功验证了通信。

## 结论

**Gemini CLI 的 ACP 消息格式兼容性问题已完全解决。**

ACP Bridge 现在可以完美支持 Gemini CLI，提供稳定的程序化 AI 代理服务。

---

*文档创建时间: 2026-04-07*
*版本: 1.0*
*状态: 进行中*
