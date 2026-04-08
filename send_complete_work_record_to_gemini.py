#!/usr/bin/env python3
"""
发送ACP Bridge完整工作记录文档给Gemini CLI进行资深系统工程师review
"""

import json
import subprocess
import asyncio
import time

async def send_complete_work_record():
    """发送完整工作记录给Gemini CLI进行系统工程师review"""
    
    print("[Review] 启动Gemini CLI进行资深系统工程师review...")
    
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
                    "name": "ACP Bridge System Review",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("[Review] 初始化Gemini CLI...")
        gemini_process.stdin.write(json.dumps(init_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"[Review] ✅ 初始化成功")
        
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
        
        print("[Review] 创建会话...")
        gemini_process.stdin.write(json.dumps(session_request) + "\n")
        gemini_process.stdin.flush()
        
        response_line = gemini_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if "result" in response:
                session_id = response["result"]["sessionId"]
                print(f"[Review] ✅ 会话创建成功: {session_id}")
                
                # 3. 读取工作记录文档并发送
                try:
                    with open("d:/Gemini/agent-hand/bridge/ACP-Bridge-Complete-Work-Record.md", "r", encoding="utf-8") as f:
                        work_record_content = f.read()
                    
                    review_request = f"""
# 资深系统工程师Review请求

请以资深系统工程师的角度，对我们实施的Agent Client Protocol (ACP) Bridge系统进行全面的技术review。

## Review要求

请从以下专业角度进行评估：

### 1. 架构设计评估
- 整体架构是否合理和可扩展？
- 模块划分是否清晰和恰当？
- 技术选型是否合适？
- 设计模式是否正确？

### 2. 技术实现评估
- 代码质量和工程实践
- 错误处理和异常管理
- 性能设计和优化
- 安全考虑和风险控制

### 3. 生产就绪评估
- 是否具备生产部署条件？
- 监控和运维是否到位？
- 可靠性和可用性如何？
- 需要哪些改进？

### 4. 最佳实践对比
- 与行业标准对比
- 最佳实践遵循情况
- 改进建议和优先级
- 技术债务管理

### 5. 未来发展建议
- 技术演进方向
- 架构升级路径
- 团队能力建设
- 风险缓解策略

## 完整工作记录

以下是我们在Windows环境下实施ACP Bridge系统的完整工作记录：

{work_record_content}

## 期待您的专业意见

作为资深系统工程师，您的专业意见将对我们的项目完善至关重要。请提供具体、可操作的建议和改进方案。

特别关注：
- 生产环境部署的可行性
- 系统架构的长期可维护性  
- 技术风险和缓解策略
- 性能优化和扩展性

感谢您的专业review！
"""
                
                    prompt_request = {
                        "jsonrpc": "2.0",
                        "id": "3",
                        "method": "session/prompt",
                        "params": {
                            "sessionId": session_id,
                            "prompt": [
                                {
                                    "type": "text",
                                    "text": review_request
                                }
                            ]
                        }
                    }
                    
                    print("[Review] 发送完整工作记录给Gemini CLI进行系统工程师review...")
                    gemini_process.stdin.write(json.dumps(prompt_request) + "\n")
                    gemini_process.stdin.flush()
                    
                    print("[Review] ⏰ 等待Gemini CLI的资深系统工程师review...")
                    
                    # 读取响应，等待45秒
                    start_time = time.time()
                    timeout = 45
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
                                        print(f"[Review] 📡 收到review片段: {chunk_text[:50]}...")
                                continue
                            
                            # 处理最终响应
                            if "result" in response:
                                final_response = response["result"]
                                elapsed = time.time() - start_time
                                print(f"[Review] 🎉 收到Gemini CLI系统工程师review! (耗时: {elapsed:.1f}秒)")
                                print("=" * 120)
                                print("👨‍💻 资深系统工程师的专业Review意见:")
                                print("=" * 120)
                                
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
                                
                                print("=" * 120)
                                print("[Review] ✅ 资深系统工程师review完成!")
                                break
                            
                            elif "error" in response:
                                print(f"[Review] ❌ 错误响应: {response['error']}")
                                break
                        
                        except json.JSONDecodeError as e:
                            print(f"[Review] JSON解析错误: {e}")
                            continue
                        except Exception as e:
                            print(f"[Review] 响应处理错误: {e}")
                            continue
                    
                    if not final_response:
                        print(f"[Review] ⚠️ {timeout}秒内未收到完整review")
                        if accumulated_response:
                            print(f"[Review] 📄 但收到了部分review: {accumulated_response[:300]}...")
                
                except FileNotFoundError:
                    print("[Review] ❌ 工作记录文档未找到")
                except Exception as e:
                    print(f"[Review] ❌ 读取文档错误: {e}")
        
        print("[Review] 系统工程师review会话结束")
        
    except Exception as e:
        print(f"[Review] 错误: {e}")
        # 读取错误信息
        if gemini_process.stderr:
            error_output = gemini_process.stderr.read()
            print(f"[Review] Gemini CLI错误输出: {error_output}")
    
    finally:
        # 清理
        print("[Review] 🧹 清理Gemini CLI进程...")
        gemini_process.terminate()
        try:
            gemini_process.wait(timeout=5)
            print("[Review] ✅ Gemini CLI进程已停止")
        except subprocess.TimeoutExpired:
            print("[Review] ⚠️ 强制停止Gemini CLI进程")
            gemini_process.kill()

if __name__ == "__main__":
    asyncio.run(send_complete_work_record())
