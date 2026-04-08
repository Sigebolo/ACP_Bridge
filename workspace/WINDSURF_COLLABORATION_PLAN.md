# Atom ↔ Windsurf 协作方案

## 📋 目标
建立 Atom（OpenClaw PM）与 Windsurf（Dev Agent）之间的标准化协作流程。

---

## 🔄 协作模式

### 模式 1：Bridge 文件同步（推荐）
**适用场景**：长期任务、需要持续监控的开发工作

**工作流程**：
1. **Atom 创建任务** → 写入 Bridge 任务文件
2. **Atom 通知 Windsurf** → 通过 RPA 发送消息到 Windsurf 聊天窗口
3. **Windsurf 执行任务** → 定期更新状态文件、进度文件
4. **Atom 监控进度** → 每 3 分钟检查状态，重大变化时报告
5. **Atom 批准请求** → 每 1 分钟检查是否需要 Alt+Enter 批准

**文件结构**：
```
D:\Gemini\agent-hand\bridge\workspace\
├── BRIDGE_COMMUNICATION_RULES.md    # 通讯规则（标准模板）
├── windsurf_tasks\
│   ├── {task_id}.md                 # 任务详情
│   └── {task_id}_status.json        # 状态文件
└── {PROJECT}_DELIVERY\
    ├── PROGRESS.md                  # 进度跟踪
    ├── BLOCKERS.md                  # 阻塞问题
    └── [交付物目录]
```

**Atom 端脚本**：
- `pm_approve.py` - 批准循环（1分钟）
- `pm_monitor.py` - 监控循环（3分钟）
- `pm_notify_windsurf.py` - 通知 Windsurf（待创建）

---

### 模式 2：直接 RPA 交互
**适用场景**：快速问答、临时指令、紧急沟通

**工作流程**：
1. **Atom 聚焦 Windsurf 窗口** → 使用 agent-hand 引擎
2. **Atom 定位聊天输入框** → VLM 语义定位
3. **Atom 发送消息** → 使用剪贴板粘贴（避免 IME 干扰）
4. **Windsurf 回复** → Atom 通过 VLM 读取回复（可选）

**关键技术**：
- `AutomationEngine` (agent-hand)
- `focus_window("Windsurf")`
- `click_semantic("the chat input box")`
- 剪贴板粘贴（Ctrl+V）

---

## 🛠️ 需要创建的工具

### 1. pm_notify_windsurf.py
**功能**：向 Windsurf 发送任务通知

```python
# 伪代码
async def notify_windsurf(task_id, task_file):
    engine = AutomationEngine(human_like=True)
    await engine.focus_window("Windsurf")
    
    message = f"""
    Windsurf，这是 Atom。
    
    新任务已分配：
    任务文件：{task_file}
    
    请阅读任务详情并开始执行。记得定期更新进度文件。
    """
    
    # 定位聊天框并发送
    await engine.click_semantic("the chat input box")
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
```

### 2. pm_read_windsurf_reply.py（可选）
**功能**：读取 Windsurf 的回复消息

```python
# 使用 VLM 截图识别最新消息
```

---

## 📝 通讯协议

### Windsurf 端规则
1. **任务开始时**：
   - 读取任务文件
   - 创建状态文件（status: in_progress, progress: 0）
   - 创建 PROGRESS.md 和 BLOCKERS.md

2. **工作期间**：
   - 每 30 分钟更新状态文件
   - 每完成子任务立即更新 PROGRESS.md
   - 遇到阻塞立即记录到 BLOCKERS.md

3. **任务完成时**：
   - 更新状态文件（status: completed, progress: 100）
   - 所有交付物放入交付目录
   - 在聊天中通知 Atom

### Atom 端规则
1. **监控循环**（3分钟）：
   - 读取状态文件、进度文件、阻塞文件
   - 检测重大变化（完成、进度+20%、新阻塞）
   - 只在重大变化时报告给天马博士

2. **批准循环**（1分钟）：
   - 检查最后更新时间
   - 如果 5 分钟内无更新，发送 Alt+Enter 批准

3. **报告规则**：
   - 任务完成 → 立即报告
   - 新阻塞问题 → 立即报告
   - 进度里程碑（每20%）→ 报告
   - 任务失败/被阻塞 → 立即报告

---

## 🧪 联调测试计划

### 测试 1：任务分配与通知
1. Atom 创建测试任务文件
2. Atom 通过 RPA 通知 Windsurf
3. 验证 Windsurf 收到消息

### 测试 2：状态文件同步
1. Windsurf 创建并更新状态文件
2. Atom 监控脚本读取状态
3. 验证 Atom 正确识别状态变化

### 测试 3：批准机制
1. Windsurf 触发需要批准的操作
2. Atom 检测到需要批准
3. Atom 发送 Alt+Enter
4. 验证 Windsurf 收到批准

### 测试 4：完整工作流
1. Atom 分配真实任务
2. Windsurf 执行并更新进度
3. Atom 监控并在完成时报告
4. 验证交付物完整性

---

## 📌 下一步行动

1. **创建 pm_notify_windsurf.py** - 任务通知脚本
2. **测试 Windsurf 窗口聚焦** - 验证 agent-hand 能否正确聚焦
3. **测试聊天框定位** - 验证 VLM 能否找到输入框
4. **创建测试任务** - 小型测试任务验证整个流程
5. **联调验证** - 与 Windsurf 实际联调

---

**创建时间**：2026-02-22 22:52
**创建者**：Atom
**状态**：待实施
