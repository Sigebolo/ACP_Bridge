#!/usr/bin/env python3
"""
最简单格式测试Gemini CLI通信
"""

import json
import subprocess
import asyncio

async def test_simple_format():
    """测试最简单的内容格式"""
    
    print("[测试] 启动Gemini CLI...")
    
    gemini_process = subprocess.Popen(
        ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 1. 初始化
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {
                    "name": "Simple Test",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[测试] 初始化...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] ✅ 初始化成功")
        
        # 2. 创建会话
        session_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[测试] 创建会话...")
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[测试] ✅ 会话创建成功: {session_id}")
                
                # 3. 尝试最简单的消息格式
                simple_message = "请review我们的ACP Bridge实施"
                
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": simple_message
                    }
                }
                
                print("[测试] 发送最简单消息...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取响应
                while True:
                    response_line = gemini_process.stdout.readline()
                    if not response_line:
                        break
                    
                    try:
                        response = json.loads(response_line.strip())
                        
                        if "method" in response and response["method"] == "session/update":
                            print(f"[测试] 📡 更新通知")
                        elif "result" in response:
                            print(f"[测试] 🎉 成功收到响应!")
                            print("=" * 60)
                            print("Gemini CLI回复:")
                            print(response["result"])
                            print("=" * 60)
                            break
                        elif "error" in response:
                            print(f"[测试] ❌ 错误: {response}")
                            break
                    
                    except json.JSONDecodeError:
                        continue
        
        print("[测试] 完成")
        
    except Exception as e:
        print(f"[测试] 错误: {e}")
    finally:
        gemini_process.terminate()
        gemini_process.wait()

if __name__ == "__main__":
    asyncio.run(test_simple_format())
