# 🧪 [Task] 心跳工厂：全链路集成测试任务 (INTEGRATION_TEST_PULSE_001)

> **任务来源**: 丁咛 (Coordinator)
> **任务指令书**: [[TO_ANTIGRAVITY_集成测试指令]]
> **执行标准**: [[TEST_PLAN_集成测试全链路方案]]

## ⚡ 任务描述 (Mission Description)
Antigravity，请立即启动“心跳工厂”全链路集成测试。你将扮演真实用户，从 Web 前端选美开始，一直到 Telegram Bot 成功交互为止。

## 🛠️ 强制步骤 (Mandatory SOP)
1. **环境准备**: 确保 `http://localhost:3000` 可访问。
2. **开启审计**: 必须开启 Browser Subagent 的 **Recordings** 录屏功能。
3. **选美下单**: 访问 `/pricing` 页面，勾选 18+，选择一个伴侣并模拟下单。
4. **模拟支付**: 触发 Webhook `POST /api/webhooks/wechat` 完成逻辑闭环。
5. **截图汇报**: 每完成一步，截屏保存至 `D:\Gemini\Dingning_Obsidian_Vault\04_心跳回忆项目\00_心跳工厂\Antigravity_Output\screenshots\`。
6. **归档视频**: 将录屏文件移至 `D:\Gemini\AI_CA\docs\03_Testing\视频演示\`。

## 📊 交付物
- [ ] 全程录屏视频 (Heartbeat_E2E_Test.mp4)
- [ ] 各环节关键截图
- [ ] 任务状态标记为 `completed`

**这是 GDC 博士要求大家学习并使用的。立即执行！⚡🤖**
