#!/usr/bin/env python3
"""
Debug the exact error from Claude Agent by capturing stderr properly
"""

import json
import subprocess
import asyncio
import time

async def debug_claude_error():
    """Debug by capturing both stdout and stderr separately"""

    print("[Debug] Starting Claude Agent ACP...")

    # 启动Claude Agent ACP进程
    claude_process = subprocess.Popen(
        ["node", "d:/Gemini/agent-hand/claude-agent-acp/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace',
        bufsize=0
    )

    stderr_output = []

    def stderr_reader():
        while True:
            line = claude_process.stderr.readline()
            if not line:
                break
            stderr_output.append(line)
            print("[Claude STDERR]: {}".format(line.rstrip()))

    import threading
    stderr_thread = threading.Thread(target=stderr_reader, daemon=True)
    stderr_thread.start()

    try:
        # 1. 初始化Claude Agent
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {
                    "name": "Debug Client",
                    "version": "1.0.0"
                },
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }

        print("[Debug] Sending initialization request...")
        claude_process.stdin.write(json.dumps(init_request) + "\n")
        claude_process.stdin.flush()

        # 读取初始化响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Debug] Initialization successful: {}".format(response.get('result', {}).get('agentInfo', {})))

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

        print("[Debug] Sending session creation request...")
        claude_process.stdin.write(json.dumps(session_request) + "\n")
        claude_process.stdin.flush()

        # 读取会话响应
        response_line = claude_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("[Debug] Session response: {}".format(response))

            if "result" in response:
                session_id = response["result"].get("sessionId", "unknown")
                print("[Debug] Session created successfully: {}".format(session_id))

                # 3. 发送测试消息 - 让我们看看Claude到底在抱怨什么
                test_message = {
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
                                        "text": "Test"
                                    }
                                ]
                            }
                        ]
                    }
                }

                print("[Debug] Sending test message...")
                claude_process.stdin.write(json.dumps(test_message) + "\n")
                claude_process.stdin.flush()

                # 等待响应
                start_time = time.time()
                while time.time() - start_time < 10:
                    # 读取stdout
                    response_line = claude_process.stdout.readline()
                    if response_line:
                        try:
                            response = json.loads(response_line.strip())
                            print("[Debug] STDOUT Response: {}".format(response))

                            if "result" in response:
                                print("[Debug] [SUCCESS] Got result!")
                                return True
                            elif "error" in response:
                                print("[Debug] [ERROR] Got error: {}".format(response["error"]))
                                # 这里就是我们需要的信息！
                                return False

                        except json.JSONDecodeError:
                            if response_line.strip():
                                print("[Debug] [INFO] Non-JSON stdout: {}".format(response_line.strip()))

                    await asyncio.sleep(0.1)

    except Exception as e:
        print("[Debug] [ERROR] Exception: {}".format(e))
        import traceback
        traceback.print_exc()

    finally:
        # 清理
        print("[Debug] [CLEANUP] Cleaning up...")
        try:
            claude_process.terminate()
            claude_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            claude_process.kill()
        except:
            pass

        # 打印所有stderr输出
        if stderr_output:
            print("[Debug] Final STDERR output:")
            for line in stderr_output:
                print("[Claude STDERR]: {}".format(line.rstrip()))

    return False

if __name__ == "__main__":
    success = asyncio.run(debug_claude_error())
    print("\n[Debug] Result: {}".format("SUCCESS" if success else "FAILED"))