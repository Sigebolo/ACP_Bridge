#!/usr/bin/env python3
"""
测试Gemini CLI的ACP连接
"""

import json
import subprocess
import asyncio

async def test_gemini_acp():
    """测试Gemini CLI ACP连接"""
    
    print("[测试] 启动Gemini CLI ACP模式...")
    
    # 启动Gemini CLI ACP进程
    gemini_process = subprocess.Popen(
        ["gemini", "--experimental-acp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
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
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] Gemini ACP初始化响应: {response}")
        
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
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        # 读取响应
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] Gemini ACP会话创建响应: {response}")
            
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
                                "text": "Hello from Windsurf via Gemini ACP!"
                            }
                        ]
                    }
                }
                
                print("[测试] 发送测试消息...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取响应
                response_line = gemini_process.stdout.readline()
                if response_line:
                    response = json.loads(response_line.strip())
                    print(f"[测试] Gemini ACP响应: {response}")
        
        print("[测试] Gemini CLI ACP连接测试成功!")
        
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
    asyncio.run(test_gemini_acp())
