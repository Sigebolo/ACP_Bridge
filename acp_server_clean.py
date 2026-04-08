#!/usr/bin/env python3
"""
ACP Agent Server for Antigravity Integration - Clean Version
"""

import asyncio
import json
import sys
import os
import argparse
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

class ACPServer:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.agents: Dict[str, Dict] = {}
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ACP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        print(f"[ACP] Received request: {method}")
        
        if method == "initialize":
            return await self.handle_initialize(params, request_id)
        elif method == "session/new":
            return await self.handle_session_new(params, request_id)
        elif method == "session/prompt":
            return await self.handle_session_prompt(params, request_id)
        elif method == "session/load":
            return await self.handle_session_load(params, request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
    
    async def handle_initialize(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Initialize connection"""
        client_info = params.get("clientInfo", {})
        print(f"[ACP] Client initialization: {client_info}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024",
                "capabilities": {
                    "tools": True,
                    "streaming": True
                },
                "serverInfo": {
                    "name": "ACP Bridge Server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def handle_session_new(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Create new session"""
        session_id = str(uuid.uuid4())
        agent_name = params.get("agent", "Gemini CLI")
        
        self.sessions[session_id] = {
            "id": session_id,
            "agent": agent_name,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        print(f"[ACP] New session created: {session_id} for {agent_name}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "status": "created"
            }
        }
    
    async def handle_session_prompt(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Handle session prompt"""
        session_id = params.get("sessionId")
        prompt = params.get("prompt", [])
        
        if session_id not in self.sessions:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32001, "message": "Session not found"}
            }
        
        print(f"[ACP] Prompt received for session {session_id}")
        
        # Process prompt (simplified for demo)
        response_content = f"Received prompt with {len(prompt)} parts"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "response": response_content,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    async def handle_session_load(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """Load existing session"""
        session_id = params.get("sessionId")
        
        if session_id not in self.sessions:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32001, "message": "Session not found"}
            }
        
        session = self.sessions[session_id]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "session": session
            }
        }

def bootstrap_install():
    """Bootstrap installation - Agent self-installation protocol"""
    print("[ACP Bootstrap] Starting Agent self-installation...")
    
    # 1. Create ACP agents config
    acp_config = {
        "agents": [
            {
                "name": "Gemini CLI",
                "command": ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
                "capabilities": ["file_access", "terminal", "tools", "streaming"]
            }
        ],
        "defaultAgent": "Gemini CLI"
    }
    
    config_path = "d:/Gemini/agent-hand/bridge/acp_agents_config.json"
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(acp_config, f, indent=2, ensure_ascii=False)
        print(f"[ACP Bootstrap] Created config: {config_path}")
    except Exception as e:
        print(f"[ACP Bootstrap] Failed to create config: {e}")
        return False
    
    # 2. Create hooks config for Windsurf
    hooks_config = {
        "hooks": {
            "post_read_code": [
                {
                    "command": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event read --file {{file}} --content {{content}}"
                }
            ],
            "post_write_code": [
                {
                    "command": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event write --file {{file}} --diff {{diff}}"
                }
            ],
            "post_run_command": [
                {
                    "command": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event cmd --command {{command}} --output {{output}}"
                }
            ],
            "post_mcp_tool_use": [
                {
                    "command": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event mcp --tool {{tool}} --result {{result}}"
                }
            ],
            "post_cascade_response": [
                {
                    "command": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event response --reasoning {{reasoning}}"
                }
            ]
        }
    }
    
    hooks_path = "d:/Gemini/agent-hand/bridge/config/hooks.json"
    try:
        os.makedirs(os.path.dirname(hooks_path), exist_ok=True)
        with open(hooks_path, 'w', encoding='utf-8') as f:
            json.dump(hooks_config, f, indent=2, ensure_ascii=False)
        print(f"[ACP Bootstrap] Created hooks config: {hooks_path}")
    except Exception as e:
        print(f"[ACP Bootstrap] Failed to create hooks: {e}")
        return False
    
    # 3. Create necessary directories
    directories = [
        "d:/Gemini/agent-hand/bridge/logs",
        "d:/Gemini/agent-hand/bridge/windsurf_notifications", 
        "d:/Gemini/agent-hand/bridge/gemini_responses"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"[ACP Bootstrap] Created directory: {directory}")
        except Exception as e:
            print(f"[ACP Bootstrap] Failed to create directory {directory}: {e}")
    
    print("[ACP Bootstrap] Installation complete!")
    print("[ACP Bootstrap] Ready for ACP communication with Gemini CLI")
    return True

async def server_main():
    """Original server main function"""
    server = ACPServer()
    
    print("[ACP] Antigravity ACP Server started", file=sys.stderr)
    print("[ACP] Waiting for JSON-RPC requests...", file=sys.stderr)
    
    try:
        while True:
            # Read from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = await server.handle_request(request)
                
                # Output response to stdout
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
                
    except KeyboardInterrupt:
        print("[ACP] Server stopped", file=sys.stderr)
    except Exception as e:
        print(f"[ACP] Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="ACP Agent Server")
    parser.add_argument("--install", action="store_true", help="Bootstrap installation for Agent self-configuration")
    args = parser.parse_args()
    
    if args.install:
        return bootstrap_install()
    
    # Original server functionality
    asyncio.run(server_main())

if __name__ == "__main__":
    main()
