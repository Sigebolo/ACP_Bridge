#!/usr/bin/env python3
"""
ACP Bridge Manager - Fixed Version
"""

import json
import subprocess
import asyncio
import sys
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

class ACPBridgeManager:
    def __init__(self, config_path: str = "d:/Gemini/agent-hand/bridge/acp_agents_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.active_sessions: Dict[str, Dict] = {}
        self.agent_processes: Dict[str, subprocess.Popen] = {}
        self.event_queue: List[Dict] = []
        self.running = False

    def load_config(self) -> Dict[str, Any]:
        """Load ACP configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if "agents" not in config:
                    config["agents"] = []
                return config
        except Exception as e:
            print(f"[ACP Bridge] Config load failed: {e}")
            return {"agents": [], "defaultAgent": "Gemini CLI"}

    def save_config(self):
        """Save ACP configuration"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ACP Bridge] Config save failed: {e}")

    async def create_session(self, agent_name: str) -> Optional[str]:
        """Create new session with agent"""
        try:
            # Find agent configuration
            agent_config = None
            for agent in self.config.get("agents", []):
                if agent["name"] == agent_name:
                    agent_config = agent
                    break
            
            if not agent_config:
                print(f"[ACP Bridge] Agent {agent_name} not found in config")
                return None

            # Start agent process if not running
            if agent_name not in self.agent_processes:
                process = subprocess.Popen(
                    agent_config["command"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.agent_processes[agent_name] = process

            # Create session
            session_id = str(uuid.uuid4())
            self.active_sessions[session_id] = {
                "id": session_id,
                "agent": agent_name,
                "created_at": datetime.now().isoformat(),
                "messages": []
            }

            print(f"[ACP Bridge] Session created: {session_id} with {agent_name}")
            return session_id

        except Exception as e:
            print(f"[ACP Bridge] Session creation failed: {e}")
            return None

    async def send_message(self, session_id: str, message: str) -> Optional[Dict]:
        """Send message to agent session"""
        if session_id not in self.active_sessions:
            print(f"[ACP Bridge] Session {session_id} not found")
            return None

        session = self.active_sessions[session_id]
        agent_name = session["agent"]

        try:
            # Add message to session
            session["messages"].append({
                "role": "user", 
                "content": message,
                "timestamp": datetime.now().isoformat()
            })

            # Create prompt request
            request = {
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4()),
                "method": "session/prompt",
                "params": {
                    "sessionId": session_id,
                    "prompt": [{"type": "text", "text": message}]
                }
            }

            # Send to agent process
            if agent_name in self.agent_processes:
                process = self.agent_processes[agent_name]
                process.stdin.write(json.dumps(request) + "\n")
                process.stdin.flush()

                # Read response
                response_line = process.stdout.readline()
                if response_line:
                    response = json.loads(response_line.strip())
                    return response

            return None

        except Exception as e:
            print(f"[ACP Bridge] Message send failed: {e}")
            return None

    async def handle_windsurf_event(self, event_type: str, event_data: Dict[str, Any]):
        """Handle Windsurf event"""
        print(f"[ACP Bridge] Received Windsurf event: {event_type}")

        # Add event to queue
        self.event_queue.append({
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.now().isoformat()
        })

        # Get default agent
        default_agent = self.config.get("defaultAgent", "Gemini CLI")

        # Create or get session
        session_id = await self.get_or_create_session(default_agent)
        if not session_id:
            print(f"[ACP Bridge] Cannot create session")
            return

        # Build event message
        message = self.build_event_message(event_type, event_data)

        # Send message
        response = await self.send_message(session_id, message)

        if response:
            print(f"[ACP Bridge] Event handled successfully: {event_type}")
        else:
            print(f"[ACP Bridge] Event handling failed: {event_type}")

    async def get_or_create_session(self, agent_name: str) -> Optional[str]:
        """Get or create session"""
        # Find existing session
        for session_id, session in self.active_sessions.items():
            if session["agent"] == agent_name:
                return session_id

        # Create new session
        return await self.create_session(agent_name)

    def build_event_message(self, event_type: str, event_data: Dict[str, Any]) -> str:
        """Build event message"""
        if event_type == "read":
            return f"File read: {event_data.get('file', 'unknown')}"
        elif event_type == "write":
            return f"File written: {event_data.get('file', 'unknown')}"
        elif event_type == "cmd":
            return f"Command executed: {event_data.get('command', 'unknown')}"
        elif event_type == "mcp":
            return f"MCP tool used: {event_data.get('tool', 'unknown')}"
        elif event_type == "response":
            return f"Agent response: {event_data.get('reasoning', 'unknown')}"
        else:
            return f"Unknown event: {event_type}"

    async def start(self):
        """Start ACP Bridge manager"""
        self.running = True
        print("[ACP Bridge] Manager started")

    async def stop(self):
        """Stop ACP Bridge manager"""
        self.running = False
        for process in self.agent_processes.values():
            process.terminate()
        print("[ACP Bridge] Manager stopped")

# Global instance
acp_bridge = ACPBridgeManager()
