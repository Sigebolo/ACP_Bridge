# Task: HBM-ENG-001 (Autonomous Mode)
## Project: Heartbeat Memories (XTHY)
## Assignee: Windsurf Architect

### 【核心目标】
初始化核心仓库并实现基础 Heartbeat Pulse 逻辑。

### 【桥梁 (Bridge) 操作规范】
你必须通过以下协议与系统通信：
1. **任务目录**: `D:\Gemini\agent-hand\bridge\workspace\windsurf\`
2. **通信协议**: 参考 `D:\Gemini\agent-hand\bridge\workspace\BRIDGE_COMMUNICATION_RULES.md`
3. **进度汇报**: 每完成一个步骤，必须更新 `HBM-ENG-001_status.json`。
4. **阻塞处理**: 如果遇到权限或环境问题，立即写入 `BLOCKERS.md`。

### 【SOP 铁律 (V3.0)】
1. **Planner 先行**: 严禁直接写代码，必须先在 `D:\Gemini\XTHY` 下生成 `IMPLEMENTATION_PLAN_HBM_001.md`。
2. **四层降级**: 执行时严格遵守 UIA -> OCR -> VLM -> 几何锚点路径。
3. **验证循环**: `Action -> Verification -> Next`。

### 【参考文档地址】
- Bridge 说明: `D:\Gemini\agent-hand\bridge\README.md`
- ATOM 通信协议: `D:\Gemini\agent-hand\openclaw-automation\Atom-Quant\ATOM_COMM.md`
- 冠军最佳实践: `C:\Users\Administrator\.openclaw\workspace_dingning\ECC_MASTER_BEST_PRACTICE.md`

### 【主程序员丁咛的最新指令】
你现在的水平还需要磨练，我已经替你写好了核心的 `heartbeat.py`。
请你立即执行以下体力活：

1. **项目规范化**: 在 `D:\Gemini\XTHY` 下创建 `.gitignore`，忽略所有 `__pycache__` 和 `.env` 文件。
2. **结构搭建**: 确保 `src/core/`, `src/memory/`, `src/utils/` 目录都已创建。
3. **代码归位**: 将我写好的 `D:\Gemini\XTHY\skills\companion-heartbeat\heartbeat.py` 移动或复制到 `src/core/heartbeat.py`，并确保它能运行。
4. **文档编写**: 在 `README.md` 中写下项目愿景：“Heartbeat Memories - 让每一份记忆都有脉搏。”

### 【纪律要求】
每完成一项，请在对话框告诉我，并更新状态 JSON。
