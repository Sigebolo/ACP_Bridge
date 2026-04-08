#!/usr/bin/env python3
"""
修复版Claude Agent ACP通讯 - 添加必需参数
"""

import json
import subprocess
import asyncio
import time

async def connect_to_claude_acp_fixed():
    """连接Claude Agent ACP - 修复版"""

    print("[Claude ACP] Starting Claude Agent ACP (fixed version)...")

    # 启动Claude Agent ACP进程
    claude_process = subprocess.Popen(
        ["node", "d:/Gemini/agent-hand/claude-agent-acp/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # 1. 初始化Claude Agent
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

        print("[Claude ACP] Sending initialization request...")
        claude_process.stdin.write(json.dumps(init_request) + "\n")
        claude_process.stdin.flush()

        # 读取初始化响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Claude ACP] [OK] Initialization successful")
            print("[Claude ACP] Claude Agent info: {}".format(response['result']['agentInfo']))

        # 2. 创建会话（添加必需参数）
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

        print("[Claude ACP] Sending session creation request...")
        claude_process.stdin.write(json.dumps(session_request) + "\n")
        claude_process.stdin.flush()

        # 读取会话响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Claude ACP] Session response: {}".format(response))

            if "result" in response:
                session_id = response["result"].get("sessionId", "unknown")
                print("[Claude ACP] [OK] Session created successfully: {}".format(session_id))

                # 3. 向Claude介绍ACP Bridge项目
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

                print("[Claude ACP] Sending project introduction...")
                claude_process.stdin.write(json.dumps(prompt_request) + "\n")
                claude_process.stdin.flush()

                print("[Claude ACP] Waiting for Claude's 10-second feedback...")

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

                        if "method" in response and response["method"] == "session/update":
                            print("[Claude ACP] [INFO] Received update notification")
                            continue

                        elif "result" in response:
                            claude_response = response["result"]
                            elapsed = time.time() - start_time
                            print("[Claude ACP] [OK] Received Claude response! (Time: {:.1f} seconds)".format(elapsed))
                            print("=" * 100)
                            print("🤖 Claude Agent's response:")
                            print("=" * 100)

                            # 格式化输出Claude的响应
                            if isinstance(claude_response, dict):
                                if "text" in claude_response:
                                    print(claude_response["text"])
                                elif "content" in claude_response:
                                    content = claude_response["content"]
                                    if isinstance(content, list):
                                        for item in content:
                                            if isinstance(item, dict):
                                                if "text" in item:
                                                    print(item["text"])
                                                elif "type" in item and item["type"] == "text":
                                                    print(item.get("text", str(item)))
                                                else:
                                                    print(item)
                                            else:
                                                print(item)
                                    else:
                                        print(content)
                                else:
                                    print(claude_response)
                            else:
                                print(claude_response)

                            print("=" * 100)
                            print("✅ Claude Agent connection successful!")
                            break

                        elif "error" in response:
                            print("[Claude ACP] [ERROR] Error response: {}".format(response))
                            break

                        else:
                            print("[Claude ACP] [INFO] Other response: {}".format(response))

                    except json.JSONDecodeError as e:
                        print("[Claude ACP] JSON parsing error: {}".format(e))
                        continue

                    except Exception as e:
                        print("[Claude ACP] Response processing error: {}".format(e))
                        continue

                if claude_response:
                    print("[Claude ACP] [OK] Claude Agent successfully connected and responded!")
                    print("[Claude ACP] [SUCCESS] ACP Bridge + Claude Agent integration successful!")
                    print("[Claude ACP] [READY] Ready to start Windsurf + Claude real-time collaboration!")
                else:
                    print("[Claude ACP] [WARNING] No response from Claude within 15 seconds")
                    print("[Claude ACP] [INFO] Please check Claude Agent configuration")

        print("[Claude ACP] [DONE] Claude ACP connection test completed")

    except Exception as e:
        print("[Claude ACP] [ERROR] Connection error: {}".format(e))
        # 读取错误信息
        if claude_process.stderr:
            error_output = claude_process.stderr.read()
            print("[Claude ACP] Claude error output: {}".format(error_output))

    finally:
        # 清理
        print("[Claude ACP] [CLEANUP] Cleaning up Claude Agent process...")
        claude_process.terminate()
        try:
            claude_process.wait(timeout=5)
            print("[Claude ACP] [OK] Claude Agent process stopped")
        except subprocess.TimeoutExpired:
            print("[Claude ACP] [WARNING] Force stopping Claude Agent process")
            claude_process.kill()

if __name__ == "__main__":
    asyncio.run(connect_to_claude_acp_fixed())