#!/usr/bin/env python3
"""
Test Windsurf hooks functionality
"""

import asyncio
import json
import sys
import argparse
from datetime import datetime

async def test_hook_event():
    """Test hook event processing"""
    parser = argparse.ArgumentParser(description="Test Hook Handler")
    parser.add_argument("--event", required=True, help="Event type")
    parser.add_argument("--file", help="File path")
    parser.add_argument("--content", help="File content")
    parser.add_argument("--diff", help="Code diff")
    parser.add_argument("--command", help="Executed command")
    parser.add_argument("--output", help="Command output")
    parser.add_argument("--tool", help="MCP tool name")
    parser.add_argument("--result", help="MCP tool result")
    parser.add_argument("--reasoning", help="Agent reasoning")
    
    args = parser.parse_args()
    
    # Build event data
    event_data = {}
    
    if args.file:
        event_data["file"] = args.file
    if args.content:
        event_data["content"] = args.content
    if args.diff:
        event_data["diff"] = args.diff
    if args.command:
        event_data["command"] = args.command
    if args.output:
        event_data["output"] = args.output
    if args.tool:
        event_data["tool"] = args.tool
    if args.result:
        event_data["result"] = args.result
    if args.reasoning:
        event_data["reasoning"] = args.reasoning
    
    # Create log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": args.event,
        "data": event_data
    }
    
    # Save to log file
    log_file = "d:/Gemini/agent-hand/bridge/logs/hook_test.log"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        print(f"[Hook Test] Event {args.event} logged successfully")
        return True
    except Exception as e:
        print(f"[Hook Test] Error logging event {args.event}: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_hook_event())
