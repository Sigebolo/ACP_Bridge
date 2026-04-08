#!/usr/bin/env python3
"""
测试完整的ACP消息发送 - 等待完整响应
"""

import json
import subprocess
import asyncio
import time

async def test_complete_acp_with_wait():
    """测试完整的ACP消息发送 - 等待完整响应"""
    
    print("[测试] 启动Gemini CLI ACP...")
    
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
                    "name": "Test Client",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[测试] 发送初始化请求...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取初始化响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] 初始化响应: OK")
        
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
        
        print("[测试] 发送会话创建请求...")
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取会话响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[测试] 会话创建成功: {session_id}")
                
                # 3. 发送消息
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "代码写入事件:\n文件: acp_test.py\n变更:\n+print('ACP Bridge is working!')"
                                    }
                                ]
                            }
                        ]
                    }
                }
                
                print("[测试] 发送代码写入事件消息...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取所有响应（包括notifications和final response）
                while True:
                    response_line = gemini_process.stdout.readline()
                    if not response_line:
                        break
                    
                    try:
                        response = json.loads(response_line.strip())
                        
                        if "method" in response and response["method"] == "session/update":
                            print(f"[测试] 收到更新通知: {response['params']['update']['sessionUpdate']}")
                        elif "result" in response:
                            print(f"[测试] 🎉 收到最终响应!")
                            print(f"[测试] 响应内容: {response}")
                            break
                        elif "error" in response:
                            print(f"[测试] 错误响应: {response}")
                            break
                        else:
                            print(f"[测试] 其他响应: {response}")
                    
                    except json.JSONDecodeError:
                        print(f"[测试] 无法解析的响应: {response_line}")
                        continue
                
                print("[测试] 🎉 ACP消息发送完成!")
        
        print("[测试] Gemini CLI ACP测试完成!")
        
    except Exception as e:
        print(f"[测试] 错误: {e}")
        # 读取错误信息
        if gemini_process.stderr:
            error_output = gemini_process.stderr.read()
            print(f"[测试] Gemini错误: {error_output}")
    finally:
        # 清理
        gemini_process.terminate()
        gemini_process.wait()

if __name__ == "__main__":
    asyncio.run(test_complete_acp_with_wait())
