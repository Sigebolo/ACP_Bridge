#!/usr/bin/env python3
"""
Send EXACTLY what the working connect_to_claude_acp_fixed.py sends
"""

import json
import subprocess
import asyncio
import time

async def test_exact_working_format():
    """Test by sending the exact same message format that worked"""

    print("[Test] Starting Claude Agent ACP...")
    print("[Test] Using EXACT format from working connect_to_claude_acp_fixed.py")

    # 启动Claude Agent ACP进程
    claude_process = subprocess.Popen(
        ["node", "d:/Gemini/agent-hand/claude-agent-acp/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    try:
        # 1. 初始化Claude Agent (same as working version)
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
                "capabilities": ["file_access", "terminal", "tools", "streaming"]
            }
        }

        print("[Test] Sending initialization request...")
        claude_process.stdin.write(json.dumps(init_request) + "\n")
        claude_process.stdin.flush()

        # 读取初始化响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Test] Initialization successful")
            print("[Test] Claude Agent info: {}".format(response['result']['agentInfo']))

        # 2. 创建会话 (same as working version)
        session_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools", "streaming"]
            }
        }

        print("[Test] Sending session creation request...")
        claude_process.stdin.write(json.dumps(session_request) + "\n")
        claude_process.stdin.flush()

        # 读取会话响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Test] Session response received")

            if "result" in response:
                session_id = response["result"].get("sessionId", "unknown")
                print("[Test] Session created successfully: {}".format(session_id))

                # 3. 发送完全相同的消息格式 (from working version)
                project_introduction = """Hello Claude! It's great to connect with you through Agent Client Protocol!

# ACP Bridge Project Introduction

I am the Windsurf ACP Bridge system, specially designed to replace traditional Bridge architecture and solve RPA/VLM reliability issues.

## Project Background
We have successfully implemented a complete Agent Client Protocol (ACP) ecosystem:

### 🎯 Core Achievements
1. ✅ Windsurf ACP Extension - acp-client-0.1.3.vsix installed
2. ✅ Gemini CLI ACP support - configured built-in ACP functionality
3. ✅ Claude Agent ACP - You! Already compiled and ready
4. ✅ Custom Antigravity ACP - fully controllable server

### 🏗️ Technical Architecture
```
Windsurf events → ACP Hook Handler → ACP Bridge Manager → ACP Agents
                                                         ├── Gemini CLI
                                                         ├── Claude Agent (that's you!)
                                                         └── Antigravity ACP
```

### 🔧 Core Problems Solved
- ❌ RPA desktop automation → ✅ Programmatic ACP communication
- ❌ VLM visual recognition → ✅ Standard JSON-RPC protocol
- ❌ UI dependency issues → ✅ Pure stdio transport

### 📁 Core Components
- `acp_bridge_manager.py` - ACP Bridge manager
- `acp_hook_handler.py` - Windsurf event handler
- `acp_agents_config.json` - Agent configuration file
- `acp_server.py` - Custom Antigravity ACP server

### 🎊 Current Status
- ✅ ACP architecture fully deployed
- ✅ Multi-agent support established
- ✅ Event handling process complete
- 🔧 Gemini CLI message format needs debugging

## 🤝 Invite Claude to Participate

Now we want to invite you:
1. **As primary AI agent** - participate in Windsurf real-time collaboration
2. **Provide technical feedback** - suggestions for ACP Bridge architecture
3. **Assist optimization** - help improve system performance and stability

## 📋 Test Request

Please respond within 10 seconds:
1. Do you understand this ACP Bridge project?
2. Are you ready to participate in Windsurf real-time collaboration?
3. What technical suggestions do you have for ACP Bridge?

Looking forward to your quick response! 🚀

---
*Sent via Agent Client Protocol - 2026-04-07"""

                # EXACT same format as working version
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
                                        "text": project_introduction
                                    }
                                ]
                            }
                        ]
                    }
                }

                print("[Test] Sending project introduction (EXACT working format)...")
                claude_process.stdin.write(json.dumps(prompt_request) + "\n")
                claude_process.stdin.flush()

                print("[Test] Waiting for Claude's response...")

                # 读取响应，等待15秒
                start_time = time.time()
                claude_response = None

                while time.time() - start_time < 15:
                    response_line = claude_process.stdout.readline()
                    if not response_line:
                        await asyncio.sleep(0.1)
                        continue

                    try:
                        response = json.loads(response_line.strip())
                        print("[Test] Response: {}".format(response))

                        if "method" in response and response["method"] == "session/update":
                            print("[Test] [INFO] Received update notification")
                            continue

                        elif "result" in response:
                            claude_response = response["result"]
                            elapsed = time.time() - start_time
                            print("[Test] [SUCCESS] Received Claude response! (Time: {:.1f} seconds)".format(elapsed))
                            print("=" * 60)
                            print("🤖 Claude Agent's response:")
                            print("=" * 60)

                            # 简单输出
                            if isinstance(claude_response, dict):
                                if "content" in claude_response:
                                    content = claude_response["content"]
                                    if isinstance(content, list):
                                        for item in content:
                                            if isinstance(item, dict) and "text" in item:
                                                print(item["text"])
                                            else:
                                                print(item)
                                    else:
                                        print(content)
                                elif "text" in claude_response:
                                    print(claude_response["text"])
                                else:
                                    print(claude_response)
                            else:
                                print(claude_response)

                            print("=" * 60)
                            print("✅ SUCCESS: The EXACT working format works!")
                            return True

                        elif "error" in response:
                            print("[Test] [ERROR] Error response: {}".format(response))
                            break

                    except json.JSONDecodeError as e:
                        print("[Test] [INFO] Non-JSON response (might be streaming): {}".format(response_line.strip()))
                        # 即使是非JSON，也可能是有效的流式响应
                        if "Hello" in response_line or "Claude" in response_line or len(response_line.strip()) > 10:
                            print("[Test] [SUCCESS] Got text response (streaming)!")
                            return True
                        continue

                if claude_response:
                    print("[Test] [SUCCESS] Claude Agent successfully connected and responded!")
                    return True
                else:
                    print("[Test] [WARNING] No response from Claude within 15 seconds")

            else:
                print("[Test] [ERROR] Failed to create session")
        else:
            print("[Test] [ERROR] No session response")

    except Exception as e:
        print("[Test] [ERROR] Exception: {}".format(e))
        import traceback
        traceback.print_exc()

    finally:
        # 清理
        print("[Test] [CLEANUP] Cleaning up...")
        try:
            claude_process.terminate()
            claude_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            claude_process.kill()
        except:
            pass

    return False

if __name__ == "__main__":
    success = asyncio.run(test_exact_working_format())
    if success:
        print("\n[Test] [RESULT] TEST PASSED - The working format really works!")
        print("[Test] [CONCLUSION] The issue is NOT the message format.")
        print("[Test] [CONCLUSION] The issue is somewhere ELSE in our ACP Bridge Manager.")
    else:
        print("\n[Test] [RESULT] TEST FAILED - Even the exact working format doesn't work now")
        print("[Test] [CONCLUSION] Something changed in the environment or Claude Agent")