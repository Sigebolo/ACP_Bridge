#!/usr/bin/env python3
"""
直接测试修复后的ACP Bridge Manager Claude通信
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from acp_bridge_manager import ACPBridgeManager

async def test_claude_communication():
    """测试与Claude Agent的通信"""
    
    print("[测试] 开始Claude Agent通信测试...")
    
    # 创建ACP Bridge Manager实例
    bridge = ACPBridgeManager()
    
    try:
        # 启动Claude Agent
        print("[测试] 启动Claude Agent...")
        success = await bridge.start_agent("Claude Agent ACP")
        
        if not success:
            print("[测试] ❌ Claude Agent启动失败")
            return
        
        print("[测试] ✅ Claude Agent启动成功")
        
        # 创建会话
        print("[测试] 创建Claude会话...")
        session_id = await bridge.create_session("Claude Agent ACP")
        
        if not session_id:
            print("[测试] ❌ 会话创建失败")
            return
        
        print(f"[测试] ✅ 会话创建成功: {session_id}")
        
        # 发送测试消息
        print("[测试] 发送测试消息...")
        test_message = "你好Claude！这是ACP Bridge Manager的测试消息。请在10秒内回复确认收到。"
        
        response = await bridge.send_message(session_id, test_message)
        
        if response:
            print("[测试] ✅ 收到Claude回复:")
            print("=" * 60)
            print(response)
            print("=" * 60)
            print("[测试] 🎉 Claude Agent通信测试成功!")
        else:
            print("[测试] ❌ 未收到Claude回复")
        
        print("[测试] ✅ Claude Agent通信测试完成!")
        
    except Exception as e:
        print(f"[测试] ❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_claude_communication())
