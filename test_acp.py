#!/usr/bin/env python3
"""
ACP客户端测试脚本
"""

import json
import subprocess
import asyncio

async def test_acp_client():
    """测试ACP客户端连接"""
    
    # 启动ACP服务器进程
    server_process = subprocess.Popen(
        ["python", "acp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="d:/Gemini/agent-hand/bridge"
    )
    
    try:
        # 发送初始化请求
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "clientInfo": {
                    "name": "Windsurf Test Client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("[测试] 发送初始化请求...")
        server_process.stdin.write(json.dumps(init_request) + "\n")
        server_process.stdin.flush()
        
        # 读取响应
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] 初始化响应: {response}")
        
        # 发送创建会话请求
        session_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "capabilities": ["file_access", "terminal"]
            }
        }
        
        print("[测试] 发送创建会话请求...")
        server_process.stdin.write(json.dumps(session_request) + "\n")
        server_process.stdin.flush()
        
        # 读取响应
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] 会话创建响应: {response}")
            
            if "result" in response:
                session_id = response["result"]["sessionId"]
                
                # 发送测试消息
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": [
                            {
                                "type": "text",
                                "text": "Hello from Gemini CLI via ACP!"
                            }
                        ]
                    }
                }
                
                print("[测试] 发送提示消息...")
                server_process.stdin.write(json.dumps(prompt_request) + "\n")
                server_process.stdin.flush()
                
                # 读取响应
                response_line = server_process.stdout.readline()
                if response_line:
                    response = json.loads(response_line.strip())
                    print(f"[测试] 提示响应: {response}")
        
        print("[测试] ACP连接测试成功!")
        
    except Exception as e:
        print(f"[测试] 错误: {e}")
    finally:
        # 清理
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    asyncio.run(test_acp_client())
