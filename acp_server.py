#!/usr/bin/env python3
"""
ACP Agent Server for Antigravity Integration
基于Agent Client Protocol的简单服务端实现
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
        """处理ACP请求"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        print(f"[ACP] 收到请求: {method}")
        
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
        """初始化连接"""
        client_info = params.get("clientInfo", {})
        print(f"[ACP] 客户端初始化: {client_info}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "streaming": True,
                    "fileSystem": True,
                    "terminals": True,
                    "tools": True
                },
                "serverInfo": {
                    "name": "Antigravity ACP Server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def handle_session_new(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        capabilities = params.get("capabilities", [])
        
        session = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "capabilities": capabilities,
            "messages": []
        }
        
        self.sessions[session_id] = session
        
        print(f"[ACP] 创建会话: {session_id}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "capabilities": capabilities
            }
        }
    
    async def handle_session_prompt(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """处理用户提示"""
        session_id = params.get("sessionId")
        messages = params.get("messages", [])
        
        if session_id not in self.sessions:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32001, "message": "Session not found"}
            }
        
        # 添加消息到会话
        for message in messages:
            self.sessions[session_id]["messages"].append(message)
        
        # 获取最后一条用户消息
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        print(f"[ACP] 用户消息: {user_message}")
        
        # 这里应该调用Antigravity进行处理
        # 暂时返回简单响应
        response_content = f"Antigravity收到消息: {user_message}"
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "stopReason": "completed",
                "messages": [
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": response_content
                            }
                        ]
                    }
                ]
            }
        }
    
    async def handle_session_load(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """加载现有会话"""
        session_id = params.get("sessionId")
        
        if session_id not in self.sessions:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32001, "message": "Session not found"}
            }
        
        print(f"[ACP] 加载会话: {session_id}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "sessionId": session_id,
                "messages": self.sessions[session_id]["messages"]
            }
        }

async def main():
    """主函数 - 从stdin读取JSON-RPC请求"""
    server = ACPServer()
    
    print("[ACP] Antigravity ACP Server 启动", file=sys.stderr)
    print("[ACP] 等待JSON-RPC请求...", file=sys.stderr)
    
    try:
        while True:
            # 从stdin读取一行
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = await server.handle_request(request)
                
                # 输出响应到stdout
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
        print("[ACP] 服务器停止", file=sys.stderr)
    except Exception as e:
        print(f"[ACP] 错误: {e}", file=sys.stderr)

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
    
    # 3. Create diagnostic script
    diagnostic_script = '''#!/usr/bin/env python3
"""
ACP Diagnostic Tool - Self-healing for Agent connections
"""
import json
import subprocess
import os

def diagnose_acp():
    print("[ACP Diag] Checking ACP Bridge status...")
    
    # Check config files
    config_files = [
        "d:/Gemini/agent-hand/bridge/acp_agents_config.json",
        "d:/Gemini/agent-hand/bridge/config/hooks.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"[ACP Diag] OK: {config_file}")
        else:
            print(f"[ACP Diag] MISSING: {config_file}")
            return False
    
    # Test Gemini CLI
    try:
        result = subprocess.run(["npx", "@google/gemini-cli", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("[ACP Diag] OK: Gemini CLI available")
        else:
            print("[ACP Diag] ERROR: Gemini CLI not working")
            return False
    except Exception as e:
        print(f"[ACP Diag] ERROR: {e}")
        return False
    
    print("[ACP Diag] All systems ready!")
    return True

if __name__ == "__main__":
    main()
'''
    
    diagnostic_path = "d:/Gemini/agent-hand/bridge/diagnose_acp.py"
    try:
        with open(diagnostic_path, 'w', encoding='utf-8') as f:
            f.write(diagnostic_script)
        print(f"[ACP Bootstrap] Created diagnostic: {diagnostic_path}")
    except Exception as e:
        print(f"[ACP Bootstrap] Failed to create diagnostic: {e}")
        return False
    
    # 4. Create necessary directories
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

def main():
    parser = argparse.ArgumentParser(description="ACP Agent Server")
    parser.add_argument("--install", action="store_true", help="Bootstrap installation for Agent self-configuration")
    args = parser.parse_args()
    
    if args.install:
        return bootstrap_install()
    
    # Original server functionality
    asyncio.run(main())
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = await server.handle_request(request)
                
                # 输出响应到stdout
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
        print("[ACP] 服务器停止", file=sys.stderr)
    except Exception as e:
        print(f"[ACP] 错误: {e}", file=sys.stderr)
