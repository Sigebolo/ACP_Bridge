#!/usr/bin/env python3
"""
改进版Gemini CLI通讯请求 - 解决超时和响应问题
"""

import asyncio
import json
import sys
import subprocess
from datetime import datetime

async def send_simple_request():
    """发送简化请求给Gemini CLI"""
    
    print("🚀 发送简化请求给Gemini CLI")
    print("=" * 50)
    
    try:
        # 直接启动Gemini CLI
        process = subprocess.Popen(
            ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 1. 初始化
        init_msg = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {"name": "Simple Test", "version": "1.0"},
                "capabilities": ["file_access"]
            }
        }
        
        print("📤 发送初始化...")
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # 等待初始化响应
        init_response = process.stdout.readline()
        if init_response:
            print("✅ 初始化成功")
        
        # 2. 创建会话
        session_msg = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access"]
            }
        }
        
        print("📤 创建会话...")
        process.stdin.write(json.dumps(session_msg) + "\n")
        process.stdin.flush()
        
        # 等待会话响应
        session_response = process.stdout.readline()
        if session_response:
            session_data = json.loads(session_response.strip())
            session_id = session_data.get("result", {}).get("sessionId")
            print(f"✅ 会话创建成功: {session_id}")
        
        # 3. 发送简化请求
        simple_request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "session/prompt",
            "params": {
                "sessionId": session_id,
                "prompt": [
                    {
                        "type": "text",
                        "text": "作为AI代理专家，请对ACP Bridge系统提供建设性意见。重点分析：1)架构优化 2)技术改进 3)用户体验提升。请简洁回答。"
                    }
                ]
            }
        }
        
        print("📤 发送建设性意见请求...")
        process.stdin.write(json.dumps(simple_request) + "\n")
        process.stdin.flush()
        
        # 4. 读取完整响应（增加超时时间）
        print("⏰ 等待Gemini CLI响应（超时: 60秒）...")
        
        accumulated_response = ""
        start_time = datetime.now()
        timeout_seconds = 60
        
        while True:
            # 检查超时
            if (datetime.now() - start_time).total_seconds() > timeout_seconds:
                print("⏰ 超时，但继续等待...")
                timeout_seconds = 120  # 延长到2分钟
            
            # 读取一行
            line = process.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            
            try:
                response = json.loads(line.strip())
                
                # 处理流式响应
                if "method" in response and response["method"] == "session/update":
                    update = response.get("params", {}).get("update", {})
                    if update.get("sessionUpdate") == "agent_message_chunk":
                        chunk_content = update.get("content", {})
                        if isinstance(chunk_content, dict) and "text" in chunk_content:
                            chunk_text = chunk_content["text"]
                            accumulated_response += chunk_text
                            print(f"📡 收到片段: {chunk_text[:50]}...")
                    continue
                
                # 处理最终响应
                if "result" in response:
                    print("🎉 收到最终响应！")
                    
                    # 显示完整响应
                    print("\n" + "=" * 60)
                    print("🤖 Gemini CLI的建设性意见:")
                    print("=" * 60)
                    
                    if accumulated_response:
                        print(accumulated_response)
                    else:
                        print("收到响应但内容为空")
                    
                    print("=" * 60)
                    
                    # 保存响应
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"d:/Gemini/agent-hand/bridge/gemini_constructive_feedback_{timestamp}.md"
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# Gemini CLI建设性意见\n\n")
                        f.write(f"**时间**: {datetime.now().isoformat()}\n")
                        f.write(f"**会话ID**: {session_id}\n\n")
                        f.write("## 🤖 Gemini CLI的响应\n\n")
                        f.write(accumulated_response if accumulated_response else "响应内容为空")
                    
                    print(f"📁 响应已保存到: {filename}")
                    
                    # 清理
                    process.terminate()
                    return True
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON解析错误: {e}")
                print(f"原始内容: {line}")
                continue
    
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(send_simple_request())
