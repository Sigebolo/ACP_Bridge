import asyncio
from acp_bridge_manager import acp_bridge
import json

async def verify_helper_function():
    print("🚀 正在验证 ACP Bridge 辅助功能...")
    
    # 使用默认代理 (Gemini CLI)
    agent_name = "Gemini CLI"
    
    # 1. 创建会话 (这会自动启动代理进程)
    print(f"1. 尝试连接代理: {agent_name}...")
    session_id = await acp_bridge.create_session(agent_name)
    
    if not session_id:
        print("❌ 错误: 无法创建会话。请检查代理配置。")
        return

    print(f"✅ 会话创建成功: {session_id}")
    
    # 2. 发送测试消息，验证格式适配和流式响应累积
    test_msg = "你好，请回复 'ACP-BRIDGE-OK' 以确认辅助功能工作正常。"
    print(f"2. 发送测试消息: '{test_msg}'")
    
    response = await acp_bridge.send_message(session_id, test_msg)
    
    if response and "full_content" in response:
        print(f"✅ 收到完整响应: {response['full_content']}")
        if "ACP-BRIDGE-OK" in response['full_content']:
            print("\n🎉 验证成功！辅助功能工作完全正常。")
        else:
            print("\n⚠️ 收到响应但内容不匹配，请检查通信逻辑。")
    else:
        print("❌ 错误: 未能收到有效响应或响应格式错误。")

    # 3. 停止代理
    await acp_bridge.stop()

if __name__ == "__main__":
    asyncio.run(verify_helper_function())
