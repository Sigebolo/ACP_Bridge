#!/usr/bin/env python3
"""
Test to see exactly what we're sending to Claude Agent
"""

import json

# Test the exact message we're sending
test_content = "Hello Claude, this is a test message."

# This is what we're constructing in acp_bridge_manager.py for Claude Agent
prompt_request = {
    "jsonrpc": "2.0",
    "id": "test-id",
    "method": "session/prompt",
    "params": {
        "sessionId": "test-session-id",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": test_content
                    }
                ]
            }
        ]
    }
}

print("Message we're sending to Claude Agent:")
print(json.dumps(prompt_request, indent=2))

print("\n" + "="*50)
print("Let's also test what the working connect_to_claude_acp_fixed.py sends:")

# From the working file
working_prompt = {
    "jsonrpc": "2.0",
    "id": "3",
    "method": "session/prompt",
    "params": {
        "sessionId": "test-session-id",
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

print(json.dumps(working_prompt, indent=2))