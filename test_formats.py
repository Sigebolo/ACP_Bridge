#!/usr/bin/env python3
"""
Test different formats to see what Claude Agent actually accepts
"""

import json

content = "Hello Claude! Can you hear me through ACP Bridge?"

print("Testing different message formats for Claude Agent:")
print("="*60)

# Format 1: messages array (what we're currently using)
format1 = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "session/prompt",
    "params": {
        "sessionId": "test",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }
        ]
    }
}

print("Format 1 - messages array:")
print(json.dumps(format1, indent=2))

# Format 2: prompt array (what Gemini CLI uses)
format2 = {
    "jsonrpc": "2.0",
    "id": "2",
    "method": "session/prompt",
    "params": {
        "sessionId": "test",
        "prompt": [
            {
                "type": "text",
                "text": content
            }
        ]
    }
}

print("\nFormat 2 - prompt array:")
print(json.dumps(format2, indent=2))

# Format 3: prompt string (simple)
format3 = {
    "jsonrpc": "2.0",
    "id": "3",
    "method": "session/prompt",
    "params": {
        "sessionId": "test",
        "prompt": content
    }
}

print("\nFormat 3 - prompt string:")
print(json.dumps(format3, indent=2))

# Format 4: Let's look at what the ERROR message said it was expecting
# The error was: 'Invalid input: expected array, received undefined' for 'prompt'
# This suggests it WAS looking for a 'prompt' field that should be an array
# but we sent 'messages' instead

print("\n" + "="*60)
print("Based on the error: 'Invalid input: expected array, received undefined' for 'prompt'")
print("It seems Claude Agent is EXPECTING a 'prompt' field (not 'messages')")
print("And that 'prompt' field should be an ARRAY")
print("So Format 2 above is likely what we should be using for Claude Agent!")