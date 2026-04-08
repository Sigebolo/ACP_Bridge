#!/usr/bin/env python3
"""
Simple test to debug Claude Agent message format - with proper encoding handling
"""

import json
import subprocess
import asyncio
import time

async def test_simple_message():
    """Test with a very simple message to isolate the format issue"""

    print("[Test] Starting Claude Agent ACP...")

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
                    "name": "Test Client",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
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
            print("[Test] Session response: {}".format(response.get('result', {})['agentInfo']))

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

        print("[Test] Sending session creation request...")
        claude_process.stdin.write(json.dumps(session_request) + "\n")
        claude_process.stdin.flush()

        # 读取会话响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Test] Session response: {}".format(response))

            if "result" in response:
                session_id = response["result"].get("sessionId", "unknown")
                print("[Test] Session created successfully: {}".format(session_id))

                # 3. 发送简单测试消息 - 尝试不同的格式
                print("[Test] Testing message format...")

                # 格式1: 根据文档标准格式 (messages)
                test_message_1 = {
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
                                        "text": "Hello Claude, this is a test message."
                                    }
                                ]
                            }
                        ]
                    }
                }

                print("[Test] Sending message with 'messages' format...")
                claude_process.stdin.write(json.dumps(test_message_1) + "\n")
                claude_process.stdin.flush()

                # 等待响应
                start_time = time.time()
                while time.time() - start_time < 10:
                    response_line = claude_process.stdout.readline()
                    if not response_line:
                        await asyncio.sleep(0.1)
                        continue

                    try:
                        response = json.loads(response_line.strip())
                        print("[Test] Response received: {}".format(response))

                        if "result" in response:
                            print("[Test] [SUCCESS] Message sent successfully with 'messages' format!")
                            return True
                        elif "error" in response:
                            print("[Test] [ERROR] Error with 'messages' format: {}".format(response["error"]))
                            break

                    except json.JSONDecodeError as e:
                        print("[Test] [INFO] Non-JSON response (might be streaming): {}".format(response_line.strip()))
                        # 即使是非JSON，也可能是有效的流式响应
                        if "Hello" in response_line or "test" in response_line.lower():
                            print("[Test] [SUCCESS] Got text response (streaming)!")
                            return True
                        continue

                # 如果第一种格式失败，尝试第二种格式
                print("[Test] Trying alternative format with 'prompt' field...")

                # 格式2: 旧格式 (prompt)
                test_message_2 = {
                    "jsonrpc": "2.0",
                    "id": "4",
                    "method": "session/prompt",
                    "params": {
                        "sessionId": session_id,
                        "prompt": "Hello Claude, this is a test message."
                    }
                }

                print("[Test] Sending message with 'prompt' format...")
                claude_process.stdin.write(json.dumps(test_message_2) + "\n")
                claude_process.stdin.flush()

                # 等待响应
                start_time = time.time()
                while time.time() - start_time < 10:
                    response_line = claude_process.stdout.readline()
                    if not response_line:
                        await asyncio.sleep(0.1)
                        continue

                    try:
                        response = json.loads(response_line.strip())
                        print("[Test] Response received: {}".format(response))

                        if "result" in response:
                            print("[Test] [SUCCESS] Message sent successfully with 'prompt' format!")
                            return True
                        elif "error" in response:
                            print("[Test] [ERROR] Error with 'prompt' format: {}".format(response["error"]))

                    except json.JSONDecodeError as e:
                        print("[Test] [INFO] Non-JSON response (might be streaming): {}".format(response_line.strip()))
                        # 即使是非JSON，也可能是有效的流式响应
                        if "Hello" in response_line or "test" in response_line.lower():
                            print("[Test] [SUCCESS] Got text response (streaming)!")
                            return True
                        continue

            else:
                print("[Test] [ERROR] Failed to create session")

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
    success = asyncio.run(test_simple_message())
    if success:
        print("\n[Test] [RESULT] Test PASSED - Found working format!")
    else:
        print("\n[Test] [RESULT] Test FAILED - Could not find working format")