#!/usr/bin/env python3
"""
Complete test of Gemini CLI ACP communication with proper response handling
"""

import json
import subprocess
import asyncio
import time

async def test_gemini_complete():
    """Complete test of Gemini CLI ACP communication"""
    
    print("[测试] 启动Gemini CLI ACP完整测试...")
    
    # 启动Gemini CLI ACP进程
    gemini_process = subprocess.Popen(
        ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
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
                    "name": "ACP Bridge Test",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[测试] 发送初始化请求...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[测试] ✅ 初始化成功: {response['result']['agentInfo']['name']} v{response['result']['agentInfo']['version']}")
        
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
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[测试] ✅ 会话创建成功: {session_id}")
                
                # 3. 发送消息
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": [
                            {
                                "type": "text",
                                "text": "Hello Gemini CLI! This is a test message from ACP Bridge. Please respond with a simple confirmation."
                            }
                        ]
                    }
                }
                
                print("[测试] 发送测试消息...")
                gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                gemini_process.stdin.flush()
                
                # 读取响应，等待20秒
                start_time = time.time()
                timeout = 20
                accumulated_response = ""
                final_response = None
                
                while time.time() - start_time < timeout:
                    response_line = gemini_process.stdout.readline()
                    if not response_line:
                        await asyncio.sleep(0.1)
                        continue
                    
                    try:
                        response = json.loads(response_line.strip())
                        
                        # 处理流式更新
                        if "method" in response and response["method"] == "session/update":
                            update = response.get("params", {}).get("update", {})
                            if update.get("sessionUpdate") == "agent_message_chunk":
                                chunk_content = update.get("content", {})
                                if isinstance(chunk_content, dict) and "text" in chunk_content:
                                    chunk_text = chunk_content["text"]
                                    accumulated_response += chunk_text
                                    print(f"[测试] 📡 收到内容片段: {chunk_text[:50]}...")
                            continue
                        
                        # 处理最终响应
                        if "result" in response:
                            final_response = response["result"]
                            elapsed = time.time() - start_time
                            print(f"[测试] 🎉 收到最终响应! (耗时: {elapsed:.1f}秒)")
                            print("=" * 80)
                            print("🤖 Gemini CLI回复:")
                            print("=" * 80)
                            
                            # 优先显示累积的响应
                            if accumulated_response:
                                print(accumulated_response)
                            elif isinstance(final_response, dict):
                                if "text" in final_response:
                                    print(final_response["text"])
                                elif "content" in final_response:
                                    content = final_response["content"]
                                    if isinstance(content, list):
                                        for item in content:
                                            if isinstance(item, dict) and "text" in item:
                                                print(item["text"])
                                            else:
                                                print(item)
                                    else:
                                        print(content)
                                else:
                                    print(final_response)
                            else:
                                print(final_response)
                            
                            print("=" * 80)
                            print("[测试] ✅ Gemini CLI ACP通信测试成功!")
                            break
                        
                        elif "error" in response:
                            print(f"[测试] ❌ 错误响应: {response['error']}")
                            break
                    
                    except json.JSONDecodeError as e:
                        print(f"[测试] JSON解析错误: {e}")
                        continue
                    except Exception as e:
                        print(f"[测试] 响应处理错误: {e}")
                        continue
                
                if not final_response:
                    print(f"[测试] ⚠️ {timeout}秒内未收到最终响应")
                    if accumulated_response:
                        print(f"[测试] 📄 但收到了累积内容: {accumulated_response[:100]}...")
        
        print("[测试] Gemini CLI ACP测试完成")
        
    except Exception as e:
        print(f"[测试] ❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        print("[测试] 🧹 清理Gemini CLI进程...")
        gemini_process.terminate()
        try:
            gemini_process.wait(timeout=5)
            print("[测试] ✅ Gemini CLI进程已停止")
        except subprocess.TimeoutExpired:
            print("[测试] ⚠️ 强制停止Gemini CLI进程")
            gemini_process.kill()

if __name__ == "__main__":
    asyncio.run(test_gemini_complete())
