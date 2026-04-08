#!/usr/bin/env python3
"""
测试修复后的ACP Bridge Manager与Claude Agent的通信
"""

import subprocess
import asyncio
import time

async def test_acp_bridge_claude():
    """测试ACP Bridge Manager与Claude Agent的完整通信"""
    
    print("[测试] 启动ACP Bridge Manager测试...")
    
    try:
        # 测试Claude Agent ACP通信
        result = subprocess.run([
            "python", "acp_bridge_manager.py", 
            "--agent", "claude-agent-acp",
            "--test-message", "你好Claude！这是ACP Bridge Manager的测试消息。请确认收到并回复。"
        ], 
        capture_output=True, 
        text=True, 
        encoding='utf-8',
        timeout=30,
        cwd="d:/Gemini/agent-hand/bridge"
        )
        
        print(f"[测试] 返回码: {result.returncode}")
        print(f"[测试] 标准输出:")
        print(result.stdout)
        
        if result.stderr:
            print(f"[测试] 错误输出:")
            print(result.stderr)
        
        # 分析结果
        if result.returncode == 0:
            print("[测试] ✅ ACP Bridge Manager测试成功!")
        else:
            print("[测试] ❌ ACP Bridge Manager测试失败!")
            
    except subprocess.TimeoutExpired:
        print("[测试] ⏰ 测试超时 (30秒)")
    except Exception as e:
        print(f"[测试] ❌ 测试错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_acp_bridge_claude())
