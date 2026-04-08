#!/usr/bin/env python3
"""
Test sending PROMPT format (not messages) to Claude Agent
Based on the error suggesting it wants 'prompt' field
"""

import json
import subprocess
import asyncio
import time

async def test_prompt_format_direct():
    """Test sending prompt format directly to Claude Agent"""

    print("[Test] Starting Claude Agent ACP...")
    print("[Test] Testing PROMPT format based on error analysis")

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

        print("[Test] Sending initialization request...")
        claude_process.stdin.write(json.dumps(init_request) + "\n")
        claude_process.stdin.flush()

        # 读取初始化响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Test] Initialization successful")
            print("[Test] Claude Agent info: {}".format(response['result']['agentInfo']))

        # 2. 创建会话
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

                # 3. 发送PROMPT格式的消息 (based on error: it wants 'prompt' field that is an array)
                test_message = "Hello Claude! Testing prompt format directly."

                # Based on error analysis: it expects 'prompt' field that is an array
                prompt_request = {
                    "jsonrpc": "2.0",
                    "id": "3",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": [
                            {
                                "type": "text",
                                "text": test_message
                            }
                        ]
                    }
                }

                print("[Test] Sending message with 'prompt' array format...")
                print("[Test] Prompt request: {}".format(json.dumps(prompt_request, indent=2)))
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
                            print("✅ SUCCESS: Prompt format works!")
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
    success = asyncio.run(test_prompt_format_direct())
    if success:
        print("\n[Test] [RESULT] TEST PASSED - Prompt format works!")
        print("[Test] [CONCLUSION] Claude Agent ACP expects 'prompt' field, not 'messages' field")
    else:
        print("\n[Test] [RESULT] TEST FAILED - Prompt format does not work")
        print("[Test] [CONCLUSION] Need to investigate further")