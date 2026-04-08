#!/usr/bin/env python3
"""
最终ACP Bridge测试
"""

import json
import subprocess
import asyncio

async def final_acp_test():
    """最终ACP Bridge测试"""
    
    print("[最终测试] 启动Gemini CLI ACP...")
    
    # 启动Gemini CLI ACP进程
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
                    "name": "Windsurf ACP Bridge",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[最终测试] 发送初始化请求...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取初始化响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[最终测试] ✅ 初始化成功")
        
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
        
        print("[最终测试] 发送会话创建请求...")
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取会话响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[最终测试] ✅ 会话创建成功: {session_id}")
                
                # 3. 发送Windsurf事件消息
                event_message = "代码写入事件:\n文件: acp_test.py\n变更:\n+print('🎉 ACP Bridge is finally working!')"
                
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": [
                            {
                                "role": "user",
                                "content": event_message
                            }
                        ]
                    }
                }
                
                print("[最终测试] 发送Windsurf事件到Gemini CLI...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取所有响应
                final_response = None
                while True:
                    response_line = gemini_process.stdout.readline()
                    if not response_line:
                        break
                    
                    try:
                        response = json.loads(response_line.strip())
                        
                        if "method" in response and response["method"] == "session/update":
                            print(f"[最终测试] 📡 收到更新通知")
                        elif "result" in response:
                            final_response = response["result"]
                            print(f"[最终测试] 🎉 收到Gemini CLI响应!")
                            break
                        elif "error" in response:
                            print(f"[最终测试] ❌ 错误响应: {response}")
                            break
                        else:
                            print(f"[最终测试] 📄 其他响应: {response}")
                    
                    except json.JSONDecodeError:
                        continue
                
                if final_response:
                    print(f"[最终测试] 🎉🎉🎉 ACP Bridge完全成功!")
                    print(f"[最终测试] 📋 Gemini CLI响应: {final_response}")
                    print(f"[最终测试] ✨ Windsurf事件已成功通过ACP发送到Gemini CLI!")
                else:
                    print(f"[最终测试] ❌ 未收到最终响应")
        
        print("[最终测试] ACP Bridge测试完成!")
        
    except Exception as e:
        print(f"[最终测试] 错误: {e}")
    finally:
        # 清理
        gemini_process.terminate()
        gemini_process.wait()

if __name__ == "__main__":
    asyncio.run(final_acp_test())
