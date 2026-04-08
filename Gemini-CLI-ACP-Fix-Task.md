# Gemini CLI ACP 格式修复任务文档

## 🎯 任务概述

请Gemini CLI完成ACP Bridge消息格式修复，实现与Gemini CLI的完整通信。

## 📋 当前状态分析

### ✅ 已成功部分
- **初始化成功** - Gemini CLI ACP模式正常启动
- **会话创建成功** - 返回有效session_id
- **通信建立** - JSON-RPC协议连接正常

### 🔧 需要修复的问题
根据之前的测试，Gemini CLI在`session/prompt`请求中出现格式错误：

```
Invalid input: expected array, received string
```

## 🎯 具体修复任务

### 1. 问题定位
**文件位置：** `d:/Gemini/agent-hand/bridge/acp_bridge_manager.py`
**方法：** `send_message` (lines 190-198)

**当前错误格式：**
```python
prompt_request = {
    "jsonrpc": "2.0",
    "id": str(uuid.uuid4()),
    "method": "session/prompt",
    "params": {
        "sessionId": session_id,
        "prompt": content  # ❌ Gemini CLI期望数组格式
    }
}
```

### 2. 期望格式分析
根据Gemini CLI官方文档和错误信息，需要调整为：

**可能的正确格式：**
```python
prompt_request = {
    "jsonrpc": "2.0",
    "id": str(uuid.uuid4()),
    "method": "session/prompt",
    "params": {
        "sessionId": session_id,
        "prompt": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
}
```

### 3. 参考资源
- **Gemini CLI ACP文档** - `Gemini-CLI-ACP-Documentation-Analysis.md`
- **问题分析** - `Gemini-CLI-ACP-Issues.md`
- **测试脚本** - `test_simple_format.py`, `test_gemini_direct.py`

## 🔧 修复步骤

### 步骤1：分析当前格式
1. 查看`acp_bridge_manager.py`中的`send_message`方法
2. 理解当前Gemini CLI的消息格式
3. 对比官方文档中的期望格式

### 步骤2：格式调整
1. 修改`prompt`参数从字符串改为数组格式
2. 确保符合Gemini CLI的schema验证
3. 保持与其他AI代理的兼容性

### 步骤3：测试验证
1. 使用修复后的代码测试Gemini CLI通信
2. 验证10秒内能收到响应
3. 确保消息内容正确传递

### 步骤4：集成测试
1. 测试完整的Windsurf → ACP Bridge → Gemini CLI流程
2. 验证文件内容传递
3. 确认错误处理机制

## 📊 成功标准

### ✅ 修复完成标志
- [ ] Gemini CLI初始化成功
- [ ] 会话创建成功
- [ ] 消息发送成功（无格式错误）
- [ ] 10秒内收到Gemini CLI响应
- [ ] 响应内容正确显示

### 🎯 最终目标
实现完整的Windsurf + Gemini CLI实时协作：
```
Windsurf事件 → ACP Hook Handler → ACP Bridge Manager → Gemini CLI
```

## 🚀 技术要求

### 兼容性要求
- **保持Claude Agent兼容性** - 修复不能破坏Claude通信
- **保持自定义ACP兼容性** - 确保Antigravity ACP正常工作
- **统一消息格式** - 可能需要实现消息格式适配器

### 性能要求
- **响应时间** - < 10秒
- **错误处理** - 完善的异常捕获和重试
- **日志记录** - 详细的调试信息

## 📝 交付物

### 1. 修复代码
- 更新`acp_bridge_manager.py`中的`send_message`方法
- 确保Gemini CLI格式正确

### 2. 测试脚本
- 创建或更新Gemini CLI测试脚本
- 验证修复效果

### 3. 文档更新
- 更新`Gemini-CLI-ACP-Issues.md`
- 记录修复过程和最终格式

### 4. 集成验证
- 完整的端到端测试
- Windsurf事件处理验证

## 🎊 项目意义

### 重要成就
完成Gemini CLI格式修复将实现：
- **多代理ACP生态系统** - Gemini + Claude + 自定义
- **完全替代传统Bridge** - 不再依赖RPA/VLM
- **标准化AI通信** - 基于开放ACP协议
- **生产就绪系统** - 可用于实际开发工作

### 技术突破
这是从**不可靠的桌面自动化**到**标准化程序化通信**的重大升级！

## 📞 支持资源

### 可用文档
- `Gemini-CLI-ACP-Documentation-Analysis.md` - 官方文档分析
- `Gemini-CLI-ACP-Issues.md` - 问题记录
- `Claude-ACP-GitHub-Issues-Analysis.md` - GitHub问题分析

### 测试脚本
- `test_simple_format.py` - Gemini CLI格式测试
- `test_gemini_direct.py` - 直接通信测试
- `connect_to_claude_acp_fixed.py` - Claude参考实现

---

**任务优先级：高**
**预计完成时间：30分钟**
**技术难度：中等**

**请Gemini CLI完成这个关键修复，让ACP Bridge完全投入生产！** 🚀✨
