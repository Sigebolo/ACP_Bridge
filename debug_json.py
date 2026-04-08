#!/usr/bin/env python3
"""
Debug exactly what JSON we're sending to Claude Agent
"""

import json

# Recreate exactly what our code is constructing
content = "Hello Claude! Can you hear me through ACP Bridge?"

# This is what we're sending for Claude Agent ACP
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
                        "text": content
                    }
                ]
            }
        ]
    }
}

print("JSON we're sending:")
print(json.dumps(prompt_request, indent=2))

print("\n" + "="*60)
print("Let's also check what the working version sends...")

# From the working connect_to_claude_acp_fixed.py that succeeded in initialization
# Let's see if we can find what made it work...

working_content = "Hello Claude! It's great to connect with you through Agent Client Protocol!"

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
                        "text": working_content
                    }
                ]
            }
        ]
    }
}

print("Working version JSON:")
print(json.dumps(working_prompt, indent=2))

print("\n" + "="*60)
print("Difference check:")

# Are they the same structure?
import difflib

our_json = json.dumps(prompt_request, indent=2, sort_keys=True)
working_json = json.dumps(working_prompt, indent=2, sort_keys=True)

print("Our JSON length:", len(our_json))
print("Working JSON length:", len(working_json))

if our_json == working_json:
    print("JSON structures are IDENTICAL")
else:
    print("JSON structures DIFFER")
    for i, (o, w) in enumerate(zip(our_json, working_json)):
        if o != w:
            print(f"First difference at position {i}: ours='{o}' vs working='{w}'")
            break