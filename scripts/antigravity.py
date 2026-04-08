import sys
import os
import subprocess
import argparse
import json
import requests

# Unified Antigravity CLI for Synchronization Bridge
# This tool handles communication between Windsurf and Antigravity IDEs.

BRIDGE_URL = "http://localhost:33333"
CONNECTOR_URL = "http://localhost:33335"
# Search for the native Antigravity CLI binary
ANTIGRAVITY_BIN = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Antigravity', 'bin', 'antigravity.cmd')

def run_native_chat(message):
    """Uses the native Antigravity CLI IPC to inject a message directly into the chat."""
    if not os.path.exists(ANTIGRAVITY_BIN):
        print(f"[!] Native Antigravity binary not found at {ANTIGRAVITY_BIN}")
        return False
    
    try:
        # Pass the message to the native 'chat' subcommand
        print(f"[*] Injecting native chat message: {message[:50]}...")
        result = subprocess.run([ANTIGRAVITY_BIN, 'chat', message], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[!] Native chat injection failed: {e}")
        return False

def push_event(args):
    """Pushes a development event to the Bridge Server."""
    payload = {
        "event": args.event,
        "file": args.file,
        "diff": args.diff,
        "cmd": args.cmd,
        "output": args.output,
        "tool": args.tool,
        "result": args.result,
        "content": args.content,
        "reasoning": args.reasoning,
        "timestamp": "--" # Server will timestamp
    }
    
    try:
        print(f"[*] Pushing {args.event} event to Bridge ({BRIDGE_URL.split(':')[-1]})...")
        response = requests.post(f"{BRIDGE_URL}/antigravity/review-step", json=payload)
        if response.status_code == 200:
            print(f"[v] Event successfully pushed.")
            return True
        else:
            print(f"[!] Bridge error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return False

def check_status():
    """Checks the health of the Bridge and Connector servers."""
    print("--- Antigravity Sync Bridge Status ---")
    
    try:
        bridge = requests.get(f"{BRIDGE_URL}/health", timeout=2)
        print(f"[v] Bridge ({BRIDGE_URL.split(':')[-1]}): OK ({bridge.json().get('status')})")
    except:
        print(f"[x] Bridge ({BRIDGE_URL.split(':')[-1]}): OFFLINE")
        
    try:
        connector = requests.get(f"{CONNECTOR_URL}/health", timeout=2)
        print(f"[v] Connector ({CONNECTOR_URL.split(':')[-1]}): OK ({connector.json().get('status')})")
    except:
        print(f"[x] Connector ({CONNECTOR_URL.split(':')[-1]}): OFFLINE")

def main():
    parser = argparse.ArgumentParser(description="Antigravity Unified Sync CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # Push command (used by IDE hooks)
    push_parser = subparsers.add_parser("push")
    push_parser.add_argument("--event", required=True, help="Event type (write, cmd, mcp)")
    push_parser.add_argument("--file", help="Affected file path")
    push_parser.add_argument("--diff", help="Diff content")
    push_parser.add_argument("--cmd", help="Terminal command executed")
    push_parser.add_argument("--output", help="Terminal / Tool output")
    push_parser.add_argument("--tool", help="MCP tool name")
    push_parser.add_argument("--result", help="MCP tool result")
    push_parser.add_argument("--content", help="File content (read)")
    push_parser.add_argument("--reasoning", help="Agent reasoning/thought")
    
    # Chat command (used for direct AI interaction)
    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("message", help="Message to send to Antigravity AI")
    
    # Status command
    subparsers.add_parser("status")
    
    args = parser.parse_args()
    
    if args.command == "push":
        push_event(args)
    elif args.command == "chat":
        run_native_chat(args.message)
    elif args.command == "status":
        check_status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
