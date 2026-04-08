# OpenClaw 情感 TTS 使用指南 (GPT-SoVITS 版)

本指南介绍如何在 OpenClaw 中使用新部署的 GPT-SoVITS 情感语音合成系统。

## 1. 核心优势
- **极致纯净**：开源项目底层，无任何广告或隐藏水印。
- **情感丰富**：支持声音克隆，能够表现出更真实的情感起伏。
- **兼容性强**：完全兼容原有的 `/tts` 接口。

## 2. OpenClaw 配置
在您的 OpenClaw 配置文件（如 `openclaw.json`）中，确保 TTS 服务地址指向新的服务器：

```json
{
  "tts": {
    "provider": "custom",
    "url": "http://34.42.163.233:5000/tts"
  }
}
```

## 3. 角色与声音选择
通过在请求中指定 `voice` 参数来切换不同的人格：

| 角色 ID | 描述 | 情感倾向 |
| :--- | :--- | :--- |
| `guardian` | 守护者 (默认) | 沉稳、温柔、坚定 |
| `sunshine` | 阳光少女 | 活力、开朗、高涨 |
| `tsundere` | 傲娇角色 | 前期冷淡、后期娇羞 |

**使用示例 (API 调用):**
```bash
curl -X POST http://34.42.163.233:5000/tts \
     -H "Content-Type: application/json" \
     -d '{"text": "博士，今天也要加油哦！", "voice": "sunshine"}' \
     --output test_voice.wav
```

## 4. 服务器管理
新服务已集成至 `START_SERVER.bat`。

- **自动启动**：双击 `manga/START_SERVER.bat`，系统会自动拉起 GPU 服务器并检查 GPT-SoVITS 状态。
- **手动重启** (在 VM 上):
  ```bash
  # 重启桥接服务
  cd ~/GPT-SoVITS && nohup python sovits_bridge.py > ~/logs/bridge.log 2>&1 &
  ```

---
> [!TIP]
> **显存建议**：目前服务器显存充足（剩余约 15GB+），可以放心地与 Forge 同时运行。
