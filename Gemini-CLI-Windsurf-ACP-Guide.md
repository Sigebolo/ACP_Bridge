# Gemini CLI + Windsurf ACP 通讯指南 🚀

本指南详细说明了如何配置和使用 Gemini CLI 通过 Agent Client Protocol (ACP) 与 Windsurf 进行实时通讯，实现从传统的 Bridge 架构到标准化程序化通讯的升级。

## 📋 核心流程架构

```
Windsurf 事件 (Hook) → ACP Hook Handler → ACP Bridge Manager → Gemini CLI (ACP 模式)
```

---

## 🛠️ 第一阶段：基础环境配置

### 1. 验证 Gemini CLI ACP 模式
确保您的 Gemini CLI 已安装并支持实验性的 ACP 功能。
```bash
npx @google/gemini-cli --experimental-acp
```

### 2. 配置代理 (acp_agents_config.json)
确保配置文件中包含 Gemini CLI 的正确设置：
```json
{
  "agents": [
    {
      "name": "Gemini CLI",
      "command": ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
      "capabilities": ["file_access", "terminal", "tools", "streaming"]
    }
  ],
  "defaultAgent": "Gemini CLI"
}
```

---

## 🚀 第二阶段：启动与运行

### 1. 启动 ACP Bridge 管理器
运行批处理文件启动后台管理进程：
```bash
Start-ACP-Bridge.bat
```
或者手动运行：
```bash
python acp_bridge_manager.py
```

### 2. 实时通讯监控 (推荐)
为了观察 Gemini CLI 的实时思考过程和原始 JSON-RPC 数据包，请在另一个终端运行：
```bash
python acp_communication_monitor.py
```
*提示：这就像查看通讯的“黑匣子”，所有往返消息都会记录在 `acp_communication_log.txt`。*

---

## 🔗 第三阶段：配置 Windsurf 集成

### 1. 配置 Cascade Hooks
在 Windsurf 的 `settings.json` 中，将事件 Hook 指向我们的 ACP 处理程序：

```json
"windsurf.cascade.hooks": {
    "onWrite": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event write --file ${file} --diff ${diff}",
    "onCommand": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event cmd --command ${command} --output ${output}",
    "onResponse": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event response --reasoning ${reasoning}"
}
```

---

## 🧪 第四阶段：实际测试场景

### 场景 A：文件编辑触发
1. 在 Windsurf 中打开任意代码文件。
2. 进行一处代码修改并保存。
3. **观察**：`acp_communication_monitor.py` 终端应立即显示 `📤 发送: 代码写入事件`。
4. **响应**：Gemini CLI 会返回其分析，Bridge 会将其累积为完整回复。

### 场景 B：直接消息测试
运行专用测试脚本验证链路：
```bash
python test_gemini_direct.py
```

---

## 🔍 监控与调试

| 工具 | 作用 |
| :--- | :--- |
| `acp_communication_monitor.py` | 实时查看 JSON-RPC 往返数据包 |
| `acp_communication_log.txt` | 完整的历史通讯记录（BBS/Log 风格） |
| `bridge.log` | Bridge 管理器的运行状态和报错日志 |

## ⚠️ 常见问题解决 (FAQ)

**Q: 报 `Invalid input: expected array` 错误？**
A: 这是旧版格式问题。请确保使用最新的 `acp_bridge_manager.py`，它已将 `prompt` 字段适配为符合 Gemini CLI 要求的数组格式。

**Q: 响应超过 30 秒超时？**
A: Gemini 在处理复杂任务时可能耗时较长。系统已实现“超时累积”机制，即使触发超时，已收到的内容片段仍会被保留并记录。

---

**🎉 现在你已经拥有了完整的 Gemini CLI + Windsurf ACP 通讯环境！**
通过这个系统，Gemini 能够实时感知您的编程动作，并提供毫秒级的专业反馈。
