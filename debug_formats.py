#!/usr/bin/env python3
"""
Debug exactly what we're sending vs what works
"""

import json
import subprocess
import asyncio
import time

# Test what we think we're sending for Claude Agent
def test_our_format():
    content = "Hello Claude, test message"

    # This is what we're now sending for Claude Agent ACP (prompt format)
    our_format = {
        "jsonrpc": "2.0",
        "id": "test",
        "method": "session/prompt",
        "params": {
            "sessionId": "test-session",
            "prompt": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        }
    }

    print("OUR FORMAT (for Claude Agent):")
    print(json.dumps(our_format, indent=2))
    print()

    # This is what the working connect_to_claude_acp_fixed.py sends
    working_format = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "session/prompt",
        "params": {
            "sessionId": "test-session",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Hello Claude! It's great to connect with you through Agent Client Protocol!"
                        }
                    ]
                }
            ]
        }
    }

    print("WORKING FORMAT (from connect_to_claude_acp_fixed.py):")
    print(json.dumps(working_format, indent=2))
    print()

    # Let's also test what happens if we send the working format
    print("="*50)
    print("Testing if the WORKING format actually works now...")

    # Start Claude Agent
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
        # Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {"name": "Test", "version": "1.0.0"},
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        claude_process.stdin.write(json.dumps(init_req) + "\n")
        claude_process.stdin.flush()
        init_line = claude_process.stdout.readline()
        if init_line:
            init_resp = json.loads(init_line.strip())
            print("Init successful:", init_resp.get('result', {}).get('agentInfo', {}))

        # Create session
        session_req = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        claude_process.stdin.write(json.dumps(session_req) + "\n")
        claude_process.stdin.flush()
        session_line = claude_process.stdout.readline()
        if session_line:
            session_resp = json.loads(session_line.strip())
            if "result" in session_resp:
                session_id = session_resp["result"]["sessionId"]
                print("Session created:", session_id)

                # NOW TEST THE WORKING FORMAT
                print("\nSending WORKING format...")
                claude_process.stdin.write(json.dumps(working_format) + "\n")
                claude_process.stdin.flush()

                # Wait for response
                start_time = time.time()
                while time.time() - start_time < 10:
                    response_line = claude_process.stdout.readline()
                    if not response_line:
                        time.sleep(0.1)
                        continue

                    try:
                        response = json.loads(response_line.strip())
                        print("Response:", response)

                        if "result" in response:
                            print("SUCCESS: Working format still works!")
                            return True
                        elif "error" in response:
                            print("ERROR with working format:", response["error"])
                            return False

                    except json.JSONDecodeError:
                        if response_line.strip():
                            print("Non-JSON response (might be streaming):", response_line.strip())
                        continue

    except Exception as e:
        print("Error:", e)
    finally:
        claude_process.terminate()
        try:
            claude_process.wait(timeout=3)
        except:
            claude_process.kill()

    return False

if __name__ == "__main__":
    test_our_format()