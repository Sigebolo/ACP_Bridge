#!/usr/bin/env python3
import sys
import requests
import json
import argparse
from datetime import datetime

# Default configuration
BRIDGE_URL = "http://localhost:33333/antigravity/review-step"

def push_step(event_type, **kwargs):
    """
    Push a step event to the Antigravity Bridge.
    """
    payload = {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "source": "windsurf-cascade-hook",
            "version": "1.0.0"
        }
    }
    
    # Add all provided arguments to the payload
    for key, value in kwargs.items():
        if value is not None:
            # Handle potential JSON strings in result or content
            if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                try:
                    payload[key] = json.loads(value)
                except:
                    payload[key] = value
            else:
                payload[key] = value

    try:
        response = requests.post(BRIDGE_URL, json=payload, timeout=5)
        response.raise_for_status()
        print(f"[v] Successfully pushed {event_type} event to Bridge.")
    except Exception as e:
        print(f"[x] Failed to push event: {str(e)}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Windsurf Cascade Hook Push Script")
    parser.add_argument("--event", required=True, help="Event type (read, write, cmd, mcp, response)")
    parser.add_argument("--file", help="File path involved in the action")
    parser.add_argument("--content", help="Content read from file")
    parser.add_argument("--diff", help="Diff of the changes written")
    parser.add_argument("--cmd", help="Command executed")
    parser.add_argument("--output", help="Command output")
    parser.add_argument("--tool", help="MCP tool name")
    parser.add_argument("--result", help="MCP tool result")
    parser.add_argument("--reasoning", help="Agent reasoning/thought process")
    
    args = parser.parse_args()
    
    # Filter out None values
    push_step(args.event, 
              file=args.file, 
              content=args.content, 
              diff=args.diff, 
              cmd=args.cmd, 
              output=args.output, 
              tool=args.tool, 
              result=args.result, 
              reasoning=args.reasoning)

if __name__ == "__main__":
    main()
