#!/usr/bin/env python3
"""
Test script to verify the ACP Bridge fix works
Handles Unicode encoding issues for Windows console
"""

import asyncio
import sys
import os

# Set environment to handle UTF-8 better
os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(msg):
    """Print function that handles encoding issues"""
    try:
        print(msg)
    except UnicodeEncodeError:
        # Fallback to ASCII-only version
        ascii_msg = ''.join(c if ord(c) < 128 else '?' for c in msg)
        print(ascii_msg)

async def test_acp_bridge_fix():
    """Test the ACP Bridge fix for Claude Agent communication"""

    safe_print("=== Testing ACP Bridge Claude Agent Fix ===")

    # Import and test
    sys.path.append('.')
    from acp_bridge_manager import ACPBridgeManager

    bridge = ACPBridgeManager()

    # Start Claude Agent
    safe_print("1. Starting Claude Agent ACP...")
    started = await bridge.start_agent('Claude Agent ACP')
    if not started:
        safe_print("   FAIL: Could not start Claude Agent")
        return False
    safe_print("   OK: Claude Agent started")

    # Create session
    safe_print("2. Creating session...")
    session_id = await bridge.create_session('Claude Agent ACP')
    if not session_id:
        safe_print("   FAIL: Could not create session")
        return False
    safe_print("   OK: Session created: {}...".format(session_id[:8]))

    # Send message
    safe_print("3. Sending test message...")
    test_msg = "Hello Claude! This is a test from the fixed ACP Bridge. Can you hear me?"
    response = await bridge.send_message(session_id, test_msg)
    if response:
        safe_print("   OK: Message sent successfully!")
        safe_print("   Response type: {}".format(type(response)))
        if isinstance(response, dict) and 'full_content' in response:
            content = response['full_content']
            preview = content[:100] + ('...' if len(content) > 100 else '')
            safe_print("   Response preview: {}".format(preview))
        elif isinstance(response, dict):
            safe_print("   Response keys: {}".format(list(response.keys())))
        return True
    else:
        safe_print("   FAIL: Could not send message")
        return False

def main():
    try:
        result = asyncio.run(test_acp_bridge_fix())
        safe_print("")
        safe_print("=== FINAL RESULT: {} ===".format("PASS" if result else "FAIL"))
        if result:
            safe_print("🎉 SUCCESS: ACP Bridge Claude Agent communication is WORKING!")
            safe_print("🚀 The fix has been successfully applied!")
        else:
            safe_print("❌ FAILURE: The fix did not work")
        return result
    except Exception as e:
        safe_print("ERROR in test: {}".format(str(e)))
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)