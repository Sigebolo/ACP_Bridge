#!/usr/bin/env python3
"""
Test ACP Bridge Manager with Gemini CLI
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from acp_bridge_manager import ACPBridgeManager

async def test_acp_bridge_gemini():
    """Test ACP Bridge Manager with Gemini CLI"""
    
    print("[测试] 开始ACP Bridge Manager + Gemini CLI测试...")
    
    # 创建ACP Bridge Manager实例
    bridge = ACPBridgeManager()
    
    try:
        # 启动Gemini CLI
        print("[测试] 启动Gemini CLI...")
        success = await bridge.start_agent("Gemini CLI")
        
        if not success:
            print("[测试] ❌ Gemini CLI启动失败")
            return
        
        print("[测试] ✅ Gemini CLI启动成功")
        
        # 创建会话
        print("[测试] 创建Gemini CLI会话...")
        session_id = await bridge.create_session("Gemini CLI")
        
        if not session_id:
            print("[测试] ❌ 会话创建失败")
            return
        
        print(f"[测试] ✅ 会话创建成功: {session_id}")
        
        # 发送测试消息
        print("[测试] 发送测试消息...")
        test_message = "你好Gemini CLI！这是ACP Bridge Manager的测试消息。请确认收到并回复。"
        
        response = await bridge.send_message(session_id, test_message)
        
        if response:
            print("[测试] ✅ 收到Gemini CLI回复:")
            print("=" * 60)
            if isinstance(response, dict):
                if "full_content" in response:
                    print(response["full_content"])
                elif "text" in response:
                    print(response["text"])
                elif "content" in response:
                    content = response["content"]
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and "text" in item:
                                print(item["text"])
                            else:
                                print(item)
                    else:
                        print(content)
                else:
                    print(response)
            else:
                print(response)
            print("=" * 60)
            print("[测试] 🎉 ACP Bridge Manager + Gemini CLI通信测试成功!")
        else:
            print("[测试] ❌ 未收到Gemini CLI回复")
        
        print("[测试] ✅ ACP Bridge Manager测试完成!")
        
    except Exception as e:
        print(f"[测试] ❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_acp_bridge_gemini())
