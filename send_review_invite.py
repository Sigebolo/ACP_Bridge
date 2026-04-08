#!/usr/bin/env python3
"""
ACP Bridge Review Invite - Gemini CLI Code Review
"""

import asyncio
import json
import sys
import subprocess
from datetime import datetime

async def send_review_invite():
    """ACP Bridge Review Invite - Gemini CLI Code Review"""
    
    print("## ACP Bridge Review Invite ##")
    print("=" * 60)
    print("## Gemini CLI Code Review ##")
    print("=" * 60)
    
    try:
        # Start Gemini CLI
        process = subprocess.Popen(
            ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # 1. Initialize
        init_msg = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": 1,
                "clientInfo": {"name": "ACP Bridge Review", "version": "1.0"},
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("1. Initialize ACP session...")
        process.stdin.write(json.dumps(init_msg) + "\n")
        process.stdin.flush()
        
        # Wait for init response
        init_response = process.stdout.readline()
        if init_response:
            print("   ACP session initialized")
        
        # 2. Create session
        session_msg = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "session/new",
            "params": {
                "cwd": "d:/Gemini/agent-hand/bridge",
                "mcpServers": [],
                "capabilities": ["file_access", "terminal", "tools"]
            }
        }
        
        print("2. Create review session...")
        process.stdin.write(json.dumps(session_msg) + "\n")
        process.stdin.flush()
        
        # Wait for session response
        session_response = process.stdout.readline()
        if session_response:
            session_data = json.loads(session_response.strip())
            session_id = session_data.get("result", {}).get("sessionId")
            print(f"   Review session created: {session_id}")
        
        # 3. Send review request
        review_request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "session/prompt",
            "params": {
                "sessionId": session_id,
                "prompt": [
                    {
                        "type": "text",
                        "text": "## ACP Bridge Code Review Request\n\nAs a senior AI agent and system architect, please conduct a comprehensive code review of our ACP Bridge implementation.\n\n## Review Scope\n\n### Core Components\n1. **acp_bridge_manager.py** - ACP Bridge core manager\n2. **acp_hook_handler.py** - Windsorf event handler\n3. **acp_communication_monitor.py** - Communication monitor\n4. **smart_loop_detector.py** - Intelligent loop detection\n\n### Key Features Implemented\n- ACP protocol integration (JSON-RPC 2.0)\n- Multi-agent support (Gemini CLI, Claude Agent ACP)\n- Windsorf Cascade Hooks integration\n- Real-time communication monitoring\n- Intelligent workflow management\n- Quality supervision capabilities\n\n## Review Criteria\n\nPlease evaluate:\n\n### 1. Architecture & Design\n- System architecture quality\n- Component separation and modularity\n- Scalability considerations\n- Design patterns usage\n\n### 2. Code Quality\n- Code structure and organization\n- Error handling and edge cases\n- Performance considerations\n- Security best practices\n\n### 3. Implementation Quality\n- ACP protocol usage correctness\n- JSON-RPC implementation\n- Async/await usage\n- Resource management\n\n### 4. Integration Quality\n- Windsorf integration effectiveness\n- Multi-agent coordination\n- Communication reliability\n- Hook implementation\n\n### 5. User Experience\n- Configuration simplicity\n- Monitoring and debugging capabilities\n- Error messages clarity\n- Documentation quality\n\n## Expected Output\n\nPlease provide:\n\n### 1. Overall Assessment\n- Quality score (1-10)\n- Strengths identification\n- Critical issues\n- Improvement priorities\n\n### 2. Specific Recommendations\n- Code improvements (with examples)\n- Architecture optimizations\n- Best practices implementation\n- Performance enhancements\n\n### 3. Risk Assessment\n- Potential security vulnerabilities\n- Performance bottlenecks\n- Scalability limitations\n- Maintenance concerns\n\n### 4. Next Steps\n- Priority improvements\n- Implementation roadmap\n- Testing recommendations\n- Deployment considerations\n\n## Context\n\nThis ACP Bridge system represents a significant upgrade from traditional RPA/VLM automation to standardized ACP protocol communication. The goal is to provide reliable, programmatic AI agent integration for development workflows.\n\nPlease provide detailed, actionable feedback to help us improve this implementation.\n\n## Review Format\n\nPlease structure your response with clear sections and specific, actionable recommendations.\n\nThank you for your expert review!"
                    }
                ]
            }
        }
        
        print("3. Send comprehensive review request...")
        process.stdin.write(json.dumps(review_request) + "\n")
        process.stdin.flush()
        
        # 4. Read complete response (extended timeout)
        print("4. Waiting for Gemini CLI review (extended timeout: 180s)...")
        
        accumulated_response = ""
        start_time = datetime.now()
        timeout_seconds = 180  # 3 minutes
        
        while True:
            # Check timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout_seconds:
                print(f"   Review timeout after {timeout_seconds}s, but continuing to wait...")
                timeout_seconds = 300  # Extend to 5 minutes
            
            # Read line
            line = process.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            
            try:
                response = json.loads(line.strip())
                
                # Handle streaming response
                if "method" in response and response["method"] == "session/update":
                    update = response.get("params", {}).get("update", {})
                    if update.get("sessionUpdate") == "agent_message_chunk":
                        chunk_content = update.get("content", {})
                        if isinstance(chunk_content, dict) and "text" in chunk_content:
                            chunk_text = chunk_content["text"]
                            accumulated_response += chunk_text
                            print(f"   Review chunk received: {len(chunk_text)} chars")
                    continue
                
                # Handle final response
                if "result" in response:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    print(f"   Review completed in {elapsed:.1f}s!")
                    
                    # Display complete review
                    print("\n" + "=" * 80)
                    print("## Gemini CLI Code Review Results ##")
                    print("=" * 80)
                    
                    if accumulated_response:
                        print(accumulated_response)
                    else:
                        print("Review received but content appears empty")
                    
                    print("=" * 80)
                    
                    # Save review
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"d:/Gemini/agent-hand/bridge/gemini_code_review_{timestamp}.md"
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# Gemini CLI Code Review\n\n")
                        f.write(f"**Review Time**: {datetime.now().isoformat()}\n")
                        f.write(f"**Session ID**: {session_id}\n")
                        f.write(f"**Duration**: {elapsed:.1f} seconds\n\n")
                        f.write("## Review Results\n\n")
                        f.write(accumulated_response if accumulated_response else "Review content was empty")
                    
                    print(f"   Review saved to: {filename}")
                    
                    # Cleanup
                    process.terminate()
                    return True
                
            except json.JSONDecodeError as e:
                print(f"   JSON decode error: {e}")
                continue
    
    except Exception as e:
        print(f"Review request failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            process.terminate()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(send_review_invite())
