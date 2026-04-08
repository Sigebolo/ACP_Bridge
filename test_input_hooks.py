#!/usr/bin/env python3
"""
Test Input Hooks - Verify Gemini CLI can "call" Windsurf
"""

import subprocess
import time
import json
import os

def start_bridge_server():
    """Start the bridge server if not running"""
    try:
        print("Starting Bridge Server...")
        process = subprocess.Popen(
            ["node", "d:/Gemini/agent-hand/bridge/src/server.js"],
            cwd="d:/Gemini/agent-hand/bridge",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give server time to start
        time.sleep(3)
        return process
    except Exception as e:
        print(f"Failed to start server: {e}")
        return None

def test_gemini_calls():
    """Test Gemini CLI input hooks"""
    print("=== Testing Gemini CLI Input Hooks ===")
    
    try:
        # Import and use the phone
        import sys
        sys.path.append("d:/Gemini/agent-hand/bridge")
        from gemini_cli_call_example import GeminiPhone
        
        phone = GeminiPhone()
        
        # Test 1: Simple message
        print("\n1. Testing simple message...")
        success1 = phone.send_message(
            "Hello from Gemini CLI! This is a test message.",
            message_type="test"
        )
        
        # Test 2: Code review
        print("\n2. Testing code review...")
        success2 = phone.send_review(
            file_path="test_file.py",
            review_content="This is a test review. The code looks good!",
            suggestions=["Add comments", "Improve variable names"]
        )
        
        # Test 3: Suggestion
        print("\n3. Testing suggestion...")
        success3 = phone.send_suggestion(
            context="Test Context",
            suggestion="This is a test suggestion for improvement.",
            confidence=0.85
        )
        
        # Check results
        print(f"\n=== Test Results ===")
        print(f"Message test: {'PASS' if success1 else 'FAIL'}")
        print(f"Review test: {'PASS' if success2 else 'FAIL'}")
        print(f"Suggestion test: {'PASS' if success3 else 'FAIL'}")
        
        # Check if notification files were created
        notification_dir = "d:/Gemini/agent-hand/bridge/windsurf_notifications"
        if os.path.exists(notification_dir):
            notifications = os.listdir(notification_dir)
            print(f"\nNotification files created: {len(notifications)}")
            for notif in notifications[-3:]:  # Show last 3
                print(f"  - {notif}")
        
        return success1 and success2 and success3
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def cleanup():
    """Clean up test files"""
    try:
        import shutil
        notification_dir = "d:/Gemini/agent-hand/bridge/windsurf_notifications"
        if os.path.exists(notification_dir):
            shutil.rmtree(notification_dir)
            print("Cleaned up notification files")
    except Exception as e:
        print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    # Start server
    server_process = start_bridge_server()
    
    if server_process:
        try:
            # Run tests
            success = test_gemini_calls()
            
            if success:
                print("\n=== All tests passed! ===")
                print("Gemini CLI can now 'call' Windsurf!")
            else:
                print("\n=== Some tests failed ===")
                print("Check the server logs for details.")
                
        finally:
            # Clean up
            cleanup()
            # Stop server
            server_process.terminate()
            print("\nServer stopped.")
    else:
        print("Failed to start server for testing.")
